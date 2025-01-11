import discord
from discord.ui import Button

from dbconfig import DB
from src.builder import Builder

db = DB()
class BlackjackView(discord.ui.View):
    def __init__(self, game, interaction, bet, user):
        super().__init__()
        self.game = game
        self.interaction = interaction
        self.bet = bet
        self.user = user

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return

        self.game.player_hand.append(self.game.deal_card())
        player_hand_value = self.game.calculate_hand_value(self.game.player_hand)

        if player_hand_value > 21:
            self.game.game_over = True
            embed = Builder.basic_embed(
                f"Your hand: {self.game.get_hand_string(self.game.player_hand)} (Total: {player_hand_value})\n"
                "You bust! The dealer wins!"
            )
            await interaction.response.edit_message(embed=embed, view=None)
            db.take_money(self.user, self.bet)
            return

        embed = Builder.basic_embed(
            f"Your hand: {self.game.get_hand_string(self.game.player_hand)} (Total: {player_hand_value})\n"
            "Press `hit` to draw again or `stand` to stop."
        )
        self.remove_item(self.double)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stand(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return

        self.game.dealer_plays()
        player_hand_value = self.game.calculate_hand_value(self.game.player_hand)
        dealer_hand_value = self.game.calculate_hand_value(self.game.dealer_hand)

        embed = Builder.basic_embed(
            f"Your hand: {self.game.get_hand_string(self.game.player_hand)} (Total: {player_hand_value})\n"
            f"Dealer's hand: {self.game.get_hand_string(self.game.dealer_hand)} (Total: {dealer_hand_value})"
        )
        await interaction.response.edit_message(embed=embed, view=None)

        if self.game.dealer_bust():
            embed = Builder.basic_embed(
                f"Dealer busts! You win {self.bet * 2} coins!"
            )
            db.give_money(self.user, self.bet * 2)
        elif self.game.player_wins():
            embed = Builder.basic_embed(
                f"You win {self.bet * 2} coins! Congratulations!"
            )
            db.give_money(self.user, self.bet * 2)
        elif player_hand_value == dealer_hand_value:
            embed = Builder.basic_embed(
                "It's a Push! Your bet is returned to you."
            )
            db.give_money(self.user, self.bet)
        else:
            embed = Builder.basic_embed(
                "The dealer wins. Better luck next time!"
            )
            db.take_money(self.user, self.bet)

        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Double")
    async def double(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return

        if db.get_balance(self.user) < self.bet * 2:
            embed = Builder.basic_embed('Not enough balance to double!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.bet *= 2
        db.take_money(self.user, self.bet)

        self.game.player_hand.append(self.game.deal_card())
        player_hand_value = self.game.calculate_hand_value(self.game.player_hand)

        embed = Builder.basic_embed(
            f"Your hand after doubling: {self.game.get_hand_string(self.game.player_hand)} (Total: {player_hand_value})\n"
            "Your turn is over. The dealer will now play."
        )
        await interaction.response.edit_message(embed=embed, view=None)


        self.game.dealer_plays()
        dealer_hand_value = self.game.calculate_hand_value(self.game.dealer_hand)

        embed = Builder.basic_embed(
            f"Your hand: {self.game.get_hand_string(self.game.player_hand)} (Total: {player_hand_value})\n"
            f"Dealer's hand: {self.game.get_hand_string(self.game.dealer_hand)} (Total: {dealer_hand_value})"
        )
        await interaction.followup.send(embed=embed)

        if self.game.dealer_bust():
            embed = Builder.basic_embed(
                f"Dealer busts! You win {self.bet * 2} coins!"
            )
            db.give_money(self.user, self.bet * 2)
        elif self.game.player_wins():
            embed = Builder.basic_embed(
                f"You win {self.bet * 2} coins! Congratulations!"
            )
            db.give_money(self.user, self.bet * 2)
        elif player_hand_value == dealer_hand_value:
            embed = Builder.basic_embed(
                "It's a Push! Your bet is returned to you."
            )
            db.give_money(self.user, self.bet)
        else:
            embed = Builder.basic_embed(
                "The dealer wins. Better luck next time!"
            )
            db.take_money(self.user, self.bet)

        await interaction.followup.send(embed=embed)