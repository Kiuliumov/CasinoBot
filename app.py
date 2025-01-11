import asyncio

from dbconfig import DB
import discord
from discord.ext import commands

from src.blackjack import Blackjack
from src.builder import Builder
from client import client
from src.views.game_views import BlackjackView
from src.views.leaderboard_page import LeaderboardButtons
from decorators import ensure_user_in_db
db = DB()


@client.event
async def on_ready():
    await client.tree.sync()
    print('Logged in as ' + client.user.name)


@client.tree.command(name="daily", description="Gives you free money once per day!")
@ensure_user_in_db()
@discord.app_commands.checks.cooldown(1, 86400, key=lambda i: (i.guild_id, i.user.id))
async def daily(interaction: discord.Interaction):
    free_money = 500
    user_id = interaction.user.id
    result = db.give_money(user_id, free_money)

    if not result:
        embed = Builder.daily_embed(f'There was an error!')
        await interaction.response.send_message(embed=embed)

    embed = Builder.daily_embed('Enjoy your free 500 coins!')
    await interaction.response.send_message(embed=embed)


@daily.error
async def on_test_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)
        embed = Builder.daily_embed(
            f'This command is on cooldown.\nPlease try again in {hours} hours, {minutes} minutes, and {seconds} seconds.')
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='balance', description="Returns your balance")
@ensure_user_in_db()
async def balance(interaction: discord.Interaction):
    user_id = interaction.user.id
    balance = db.get_balance(user_id)
    embed = Builder.balance_embed(str(balance))
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='leaderboard', description='The leaderboard of all players in the casino bot!')
@ensure_user_in_db()
async def leaderboard(interaction: discord.Interaction):
    current_page = 1
    current_players = db.get_five_players(current_page)
    embed = Builder.create_leaderboard_embed(current_players, current_page)
    await interaction.response.send_message(embed=embed, view=LeaderboardButtons(current_page))


@client.tree.command(name='guess', description='A number guessing game')
@ensure_user_in_db()
async def guess_the_number(interaction: discord.Interaction, bet: int):
    user = interaction.user.id
    user_balance = db.get_balance(user)

    if user_balance < bet:
        embed = Builder.basic_embed('Not enough balance for this bet!')
        await interaction.response.send_message(embed=embed)
        return

    db.take_money(user, bet)

    import random
    secret_number = random.randint(1, 100)
    tries = 5

    embed = Builder.basic_embed(
        "Number Guessing Game\n\n"+
        f"I've chosen a number between 1 and 100. You have {tries} attempts to guess it.\n\nType your guess in the chat!"
    )
    await interaction.response.send_message(embed=embed)

    def check(message):
        return message.author == interaction.user and message.channel == interaction.channel

    while tries > 0:
        try:
            message = await client.wait_for('message', check=check, timeout=30.0)
            guess = int(message.content)

            if guess == secret_number:
                winnings = bet * 2
                db.give_money(user, winnings)
                embed = Builder.basic_embed(
                    "You Win!\n\n" +
                    f"Congratulations! You guessed the number {secret_number} correctly. You win {winnings} coins!"
                )
                await interaction.followup.send(embed=embed)
                return
            elif guess < secret_number:
                feedback = "Too low!"
            else:
                feedback = "Too high!"

            tries -= 1
            if tries != 0:
                embed = Builder.basic_embed(
                    "Try Again!\n\n" +
                    f"{feedback} You have {tries} attempts remaining."
                )
                await interaction.followup.send(embed=embed)
        except ValueError:
            await interaction.followup.send('Enter a valid number!')
        except asyncio.TimeoutError:
            embed = Builder.basic_embed(
                "Timeout!\n" +
                "You took too long to respond. Game over!"
            )
            await interaction.followup.send(embed=embed)
            return

    embed = Builder.basic_embed(
        "Game Over\n"+
        f"You've used all your attempts. The number was {secret_number}. Better luck next time!"
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="blackjack", description="Play a game of Blackjack")
@ensure_user_in_db()
async def blackjack(interaction: discord.Interaction, bet: int):
    user = interaction.user.id
    user_balance = db.get_balance(user)

    if user_balance < bet:
        embed = Builder.basic_embed('Not enough balance for this bet!')
        await interaction.response.send_message(embed=embed)
        return

    game = Blackjack()
    game.start_game(bet, user_balance)

    player_hand_str = game.get_hand_string(game.player_hand)
    dealer_hand_str = f"{game.dealer_hand[0]}, ?"

    embed = Builder.basic_embed(
        f"Welcome to Blackjack!\nYour bet is `{bet}`. Your balance is `{user_balance}`.\n\n"
        f"Your hand: `{player_hand_str}`\nDealer's hand: `{dealer_hand_str}`\n\n"
        "Use the buttons below to play your turn."
    ).set_image(url='https://i.postimg.cc/1tXDDWnP/output.jpg')
    view = BlackjackView(game, interaction, bet, user)
    await interaction.response.send_message(embed=embed, view=view)

@client.tree.command(name="free", description="Gives you free coins if you're amount is 0")
@ensure_user_in_db()
async def free(interaction: discord.Interaction):
    user = interaction.user
    if db.get_balance(user.id) == 0:
        db.give_money(user, 250)
        embed = Builder.basic_embed('You can have 250 free coins!')
        await interaction.response.send_message(embed=embed)
    embed = Builder.basic_embed('You are rich bro')
    await interaction.response.send_message(embed=embed)


client.run('ODM0NDg4MzQ2MTcxOTMyNzAy.G1mybh.RxakfsLva1E_2sibExxaVVuKMduJeXLd6C1jqk')
