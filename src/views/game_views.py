import discord
from discord.ui import Button
from dbconfig import DB
from src.builder import Builder
from src.translate import translate

db = DB()

class BlackjackView(discord.ui.View):
    def __init__(self, game, interaction, bet, user):
        super().__init__()
        self.game = game
        self.interaction = interaction
        self.bet = bet
        self.user = user
        self.guild_id = interaction.guild.id

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user:
            await interaction.response.send_message(translate(key="not_your_game", guild_id=self.guild_id), ephemeral=True)
            return

        self.game.player_hand.append(self.game.deal_card())
        player_hand_value = self.game.calculate_hand_value(self.game.player_hand)

        if player_hand_value > 21:
            self.game.game_over = True
            embed = Builder.basic_embed(
                f"{translate(key='blackjack_your_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.player_hand), total=player_hand_value)}\n"
                f"{translate(key='blackjack_busted', guild_id=self.guild_id, total=player_hand_value)}\n"
                f"{translate(key='blackjack_dealer_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.dealer_hand), total=self.game.calculate_hand_value(self.game.dealer_hand))}",
                guild_id=interaction.guild.id
            )
            await interaction.response.edit_message(embed=embed, view=None)
            db.take_money(self.user, self.bet)
            return

        embed = Builder.basic_embed(
            f"{translate(key='blackjack_your_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.player_hand), total=player_hand_value)}\n"
            f"{translate(key='blackjack_hit_or_stand', guild_id=self.guild_id)}\n"
            f"{translate(key='blackjack_dealer_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.dealer_hand), total=self.game.calculate_hand_value(self.game.dealer_hand))}",
            guild_id=interaction.guild.id
        )
        self.remove_item(self.double)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stand(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user:
            await interaction.response.send_message(translate(key="not_your_game", guild_id=self.guild_id), ephemeral=True)
            return

        self.game.dealer_plays()
        player_hand_value = self.game.calculate_hand_value(self.game.player_hand)
        dealer_hand_value = self.game.calculate_hand_value(self.game.dealer_hand)

        embed = Builder.basic_embed(
            f"{translate(key='blackjack_your_hand', guild_id=self.guild_id, total=player_hand_value)}\n"
            f"{translate(key='blackjack_dealer_hand', guild_id=self.guild_id,cards=self.game.get_hand_string(self.game.dealer_hand), total=dealer_hand_value)}",
            guild_id=interaction.guild.id
        )
        await interaction.response.edit_message(embed=embed, view=None)

        if self.game.dealer_bust():
            embed = Builder.basic_embed(
                f"{translate(key='blackjack_dealer_busted', guild_id=self.guild_id, total=dealer_hand_value, winnings=self.bet + self.bet)}",
                guild_id=interaction.guild.id
            )
            db.give_money(self.user, self.bet * 2)
        elif self.game.player_wins():
            embed = Builder.basic_embed(
                f"{translate(key='blackjack_win', guild_id=self.guild_id, winnings=self.bet * 2, total=player_hand_value)} {translate(key='blackjack_congratulations', guild_id=self.guild_id)}",
                guild_id=interaction.guild.id
            )
            db.give_money(self.user, self.bet * 2)
        elif player_hand_value == dealer_hand_value:
            embed = Builder.basic_embed(
                translate(key='blackjack_push', guild_id=self.guild_id),
                guild_id=interaction.guild.id
            )
            db.give_money(self.user, self.bet)
        else:
            embed = Builder.basic_embed(
                translate(key='blackjack_lose', guild_id=self.guild_id, total=dealer_hand_value),
                guild_id=interaction.guild.id
            )
            db.take_money(self.user, self.bet)

        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Double", style=discord.ButtonStyle.secondary)
    async def double(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user:
            await interaction.response.send_message(translate(key="not_your_game", guild_id=self.guild_id), ephemeral=True)
            return

        if db.get_balance(self.user) < self.bet * 2:
            embed = Builder.basic_embed(translate(key='insufficient_balance', guild_id=self.guild_id))
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.bet *= 2
        db.take_money(self.user, self.bet)

        self.game.player_hand.append(self.game.deal_card())
        player_hand_value = self.game.calculate_hand_value(self.game.player_hand)

        embed = Builder.basic_embed(
            f"{translate(key='blackjack_after_doubling', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.player_hand), total=player_hand_value)}\n"
            f"{translate(key='blackjack_dealer_now_playing', guild_id=self.guild_id)}\n"
            f"{translate(key='blackjack_dealer_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.dealer_hand), total=self.game.calculate_hand_value(self.game.dealer_hand))}",
            guild_id=interaction.guild.id
        )
        await interaction.response.edit_message(embed=embed, view=None)

        self.game.dealer_plays()
        dealer_hand_value = self.game.calculate_hand_value(self.game.dealer_hand)

        embed = Builder.basic_embed(
            f"{translate(key='blackjack_your_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.player_hand), total=player_hand_value)}\n"
            f"{translate(key='blackjack_dealer_hand', guild_id=self.guild_id, cards=self.game.get_hand_string(self.game.dealer_hand), total=dealer_hand_value)}",
            guild_id=interaction.guild.id
        )
        await interaction.followup.send(embed=embed)

        if self.game.dealer_bust():
            embed = Builder.basic_embed(
                f"{translate(key='blackjack_win', guild_id=self.guild_id, winnings=f'{self.bet * 2} :coin:', total=self.game.calculate_hand_value(self.game.player_hand))} ",
                guild_id=interaction.guild.id
            )
            db.give_money(self.user, self.bet * 2)
        elif self.game.player_wins():
            embed = Builder.basic_embed(
                f"{translate(key='blackjack_congratulations', guild_id=self.guild_id, winnings=self.bet*2)} {self.bet * 2}",
                guild_id=interaction.guild.id
            )
            db.give_money(self.user, self.bet * 2)
        elif player_hand_value == dealer_hand_value:
            embed = Builder.basic_embed(
                translate(key='blackjack_push', guild_id=self.guild_id),
                guild_id=self.guild_id
            )
            db.give_money(self.user, self.bet)
        else:
            embed = Builder.basic_embed(
                translate(key='blackjack_busted', guild_id=self.guild_id, total=self.game.calculate_hand_value(self.game.player_hand)),
                guild_id=interaction.guild.id
            )
            db.take_money(self.user, self.bet)

        await interaction.followup.send(embed=embed)
