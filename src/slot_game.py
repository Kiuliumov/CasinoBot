import os
import discord
from PIL import Image

from dbconfig import DB
from src.slot import SlotMachine
from src.slot_image import SlotMachineVisualizer

db = DB()
slot = SlotMachine()

def check_balance_decorator(bet_amount):
    def decorator(func):
        async def wrapper(self, interaction, button):
            if not check_balance(interaction.user.id, bet_amount):
                await interaction.response.send_message(f"Insufficient balance to bet {bet_amount} 🪙", ephemeral=True)
                await interaction.message.edit(view=self)
                return
            return await func(self, interaction, button)
        return wrapper
    return decorator

def check_balance(id, bet):
    balance = db.get_balance(id)
    if balance >= bet:
        db.take_money(id, bet)
        return True
    return False

class SlotPlayView(discord.ui.View):
    def __init__(self, user_id, timeout=350):
        super().__init__(timeout=timeout)
        self.user = user_id

    @discord.ui.button(label="Enter", style=discord.ButtonStyle.primary)
    async def enter(self, interaction, button):
        if interaction.user.id != self.user:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return

        spin_results, payout = slot.play(1)

        embed = discord.Embed(
            title="🎰 Slots!",
            description="Spin the reels and test your luck! 🍀\n`Your balance: " + f'{db.get_balance(self.user)}`',
            color=discord.Color.gold()
        )

        visualizer = SlotMachineVisualizer(
            background_image=os.path.abspath(os.path.join('src', 'images', 'background.jpg')),
            border_image=os.path.abspath(os.path.join('src', 'images', 'border.png'))
        )
        image_path = f'{self.user}.png'
        visualizer.generate_image(spin_results, output_path=image_path)

        file = discord.File(image_path, filename=image_path)
        embed.set_image(url=f"attachment://{file.filename}")

        embed.set_footer(
            text=f"Place your bet! | Good Luck, {interaction.user.name}! 🍀",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )

        await interaction.response.send_message(file=file, embed=embed, view=self.BetOptionsView(self.user))
        file.close()
        os.remove(image_path)

    class BetOptionsView(discord.ui.View):
        def __init__(self, user_id, timeout=350):
            super().__init__(timeout=timeout)
            self.user = user_id

        async def check_user(self, interaction):
            if interaction.user.id != self.user:
                await interaction.response.send_message("This is not your game!", ephemeral=True)
                return False
            return True

        @discord.ui.button(label="50", style=discord.ButtonStyle.primary)
        @check_balance_decorator(50)
        async def bet_50(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self.check_user(interaction):
                return
            await self.play_slot(interaction, 50)

        @discord.ui.button(label="100", style=discord.ButtonStyle.primary)
        @check_balance_decorator(100)
        async def bet_100(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self.check_user(interaction):
                return
            await self.play_slot(interaction, 100)

        @discord.ui.button(label="500", style=discord.ButtonStyle.primary)
        @check_balance_decorator(500)
        async def bet_500(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self.check_user(interaction):
                return
            await self.play_slot(interaction, 500)

        @discord.ui.button(label="1000", style=discord.ButtonStyle.primary)
        @check_balance_decorator(1000)
        async def bet_1000(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self.check_user(interaction):
                return
            await self.play_slot(interaction, 1000)

        @discord.ui.button(label="5000", style=discord.ButtonStyle.primary)
        @check_balance_decorator(5000)
        async def bet_5000(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self.check_user(interaction):
                return
            await self.play_slot(interaction, 5000)

        async def play_slot(self, interaction: discord.Interaction, bet: int):
            spin_results, payout = slot.play(bet)

            payout_amount = round(bet * payout)
            db.give_money(interaction.user.id, payout_amount)

            embed = discord.Embed(
                title="🎰 Slots!",
                description="Spin the reels and test your luck! 🍀\n`Your balance: " + f'{db.get_balance(self.user)}`',
                color=discord.Color.gold()
            )

            visualizer = SlotMachineVisualizer(
                background_image=os.path.abspath(os.path.join('src', 'images', 'background.jpg')),
                border_image=os.path.abspath(os.path.join('src', 'images', 'border.png'))
            )
            image_path = f'{self.user}.png'
            visualizer.generate_image(spin_results, output_path=image_path)

            file = discord.File(image_path, filename=image_path)
            embed.set_image(url=f"attachment://{file.filename}")

            embed.set_footer(
                text=f"Payout: {payout_amount} 🪙 | Good Luck, {interaction.user.name}! 🍀",
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None
            )

            await interaction.response.send_message(
                file=file,
                embed=embed,
                view=self
            )

            file.close()
            os.remove(image_path)