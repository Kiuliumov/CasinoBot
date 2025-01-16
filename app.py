import asyncio

from dbconfig import DB
import discord
from discord.ext import commands

from src.blackjack import Blackjack
from src.builder import Builder
from client import client
from src.views.game_views import BlackjackView
from src.views.leaderboard_page import LeaderboardButtons
from decorators import ensure_user_in_db, check_bet
from src.slot_game import SlotPlayView
from src.roulette import Roulette
import random

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

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed('Insufficient balance!')
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed('Place a positive bet!')
        await interaction.response.send_message(embed=embed)
        return

    db.take_money(user, bet)

    import random
    secret_number = random.randint(1, 100)
    tries = 5

    embed = Builder.basic_embed(
        "Number Guessing Game\n\n" +
        f"I've chosen a number between 1 and 100. You have {tries} attempts to guess it.\n\nType your guess in the chat!"
    )
    await interaction.response.send_message(embed=embed)

    def check(message):
        return message.author == interaction.user and message.channel == interaction.channel

    while tries > 0:
        print(secret_number)
        try:
            message = await client.wait_for('message', check=check, timeout=30.0)
            guess = int(message.content)

            if guess == secret_number:
                winnings = bet * 1 + tries
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
        "Game Over\n" +
        f"You've used all your attempts. The number was {secret_number}. Better luck next time!"
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="blackjack", description="Play a game of Blackjack")
@ensure_user_in_db()
async def blackjack(interaction: discord.Interaction, bet: int):
    user = interaction.user.id
    user_balance = db.get_balance(user)

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed('Insufficient balance!')
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed('Place a positive bet!')
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
        db.give_money(user.id, 250)
        embed = Builder.basic_embed('You can have 250 free coins!')
        await interaction.response.send_message(embed=embed)
    embed = Builder.basic_embed('You are rich bro')
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='slot', description='A slot machine')
@ensure_user_in_db()
async def slot(interaction: discord.Interaction):
    embed = discord.Embed(title='Welcome to slots!',
                          description='You place a bet and spin a 3x3 grid filled with different symbols. Each symbol has a payout value, and some symbols are more likely to appear than others.\n\nIf you get three matching symbols in a row, column, or diagonal, you win a payout based on the symbol\'s value. There\'s also a special symbol that can give a huge jackpot if it appears!\n\n**Those are the symbols with their multipliers:**\n').set_thumbnail(
        url='https://i.postimg.cc/zXRHmpV2/image.png')
    symbols = [
            {"symbol": "<:96706rocketbloxfruits:1327654132047286335> ", "payout": 1.1, 'weight': 10},
            {"symbol": "<:79498barrierbloxfruits:1327654390433058867> ", "payout": 1.5, "weight": 20},
            {"symbol": "<:66704lightbloxfruits:1327654746986647582> ", "payout": 5, "weight": 10},
            {"symbol": "<:27526springbloxfruits:1327667924835500074> ", "payout": 10, "weight": 5},
            {"symbol": "<:55921portalbloxfruits:1327655677534928988> ", "payout": 15, "weight": 5},
            {"symbol": "<:65717lovebloxfruits:1327655844338470973> ", "payout": 20, "weight": 4},
    ]

    for s in symbols:
        symbol = s['symbol']
        multiplier = s['payout']
        embed.add_field(name=f'{symbol} - {multiplier} multiplier!', value='', inline=False)
    embed.add_field(name='Special symbol: <:1013moneyz:1325913819335233609> - 5000 multiplier!', value='', inline=False)
    await interaction.response.send_message(embed=embed, view=SlotPlayView(interaction.user.id))

@client.tree.command(name='weekly', description='Get 50000 every week')
@discord.app_commands.checks.cooldown(1, 86400 * 7, key=lambda i: (i.guild_id, i.user.id))
@ensure_user_in_db()
async def weekly(interaction: discord.Interaction):
    free_money = 50000
    user_id = interaction.user.id
    result = db.give_money(user_id, free_money)

    if not result:
        embed = Builder.basic_embed('There was an error!')
        await interaction.response.send_message(embed=embed)
        return

    embed = Builder.weekly_embed('Enjoy your free 50000 coins!')
    await interaction.response.send_message(embed=embed)


@weekly.error
async def on_weekly_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)
        days = int(remaining_time // 86400)
        hours = int((remaining_time % 86400) // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)
        time_message = (
            f'{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds'
            if days > 0 else
            f'{hours} hours, {minutes} minutes, and {seconds} seconds'
        )
        embed = Builder.daily_embed(f'This command is on cooldown.\nPlease try again in {time_message}.')
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='gift', description='Gift money to a user')
@ensure_user_in_db()
async def gift(interaction: discord.Interaction, amount: int, user: discord.User):
    user_id = interaction.user.id

    if not db.check_if_user_is_registered(user.id):
        db.new_user(user.id)

    if user.id == user_id:
        await interaction.response.send_message("Nice try!")
        return

    user_balance = db.get_balance(user_id)
    if user.id == client.user.id:
        await interaction.response.send_message("Oops don't give me money!")
        return

    if amount > user_balance:
        embed = Builder.basic_embed('You don\'t have enough money.')
        await interaction.response.send_message(embed=embed)
        return

    db.give_money(user.id, amount)
    db.take_money(user_id, amount)

    embed = Builder.basic_embed(f'{interaction.user.display_name} gave {amount} to {user.display_name}!')

    await interaction.response.send_message(embed=embed)


@client.tree.command(name='about', description='Information about the bot')
@ensure_user_in_db()
async def about(interaction: discord.Interaction):
    embed = discord.Embed(title='About us').set_author(name=f'{client.user.name}', icon_url=client.user.avatar)
    embed.description = 'Casino is a dynamic and engaging Discord bot that brings the excitement of a virtual casino to your server. With a built-in economy system, users can earn, bet, and manage their virtual coins while participating in a variety of games like slots, blackjack, and number guessing. The bot also fosters community interaction through features like leaderboards and gifting, allowing players to compete for the top spot or share their winnings with friends. Daily and weekly bonuses, along with a safety net for those with empty wallets, ensure that everyone can join in the fun. With an easy-to-use interface and immersive gameplay, Casino transforms your server into an entertaining and interactive gaming hub.\n\nDeveloped by The Cantina'
    embed.set_image(url='https://img.freepik.com/free-vector/golden-casino-background-with-playing-cards_1017-33699.jpg')
    embed.set_footer(text = "Casino by The Cantina | Claim your reward daily!")
    await interaction.response.send_message(embed=embed)



@client.tree.command(name='coinflip', description='A coinflip command!')
@ensure_user_in_db()
async def coinflip(interaction: discord.Interaction, bet: int, prediction: str):
    if prediction != 'heads' and prediction != 'tails':
        await interaction.response.send_message('You should choose either "heads" or "tails".')
        return

    user = interaction.user.id

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed('Insufficient balance!')
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed('Place a positive bet!')
        await interaction.response.send_message(embed=embed)
        return

    computer_choice = random.randint(0, 1)
    if computer_choice == 0:
        computer_choice = 'tails'
    else:
        computer_choice = 'heads'

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed('Insufficient balance!')
        await interaction.response.send_message(embed=embed)
        return

    if computer_choice == 'heads':
        if prediction == 'heads':
            db.take_money(user, bet)
            winnings = str(bet + bet)
            embed = Builder.basic_embed('Congratulations! you win! ' + winnings + ' coins!'
                                        ).set_image(url='https://sciencegems.wordpress.com/wp-content/uploads/2022/04/heads-coinflip.gif')
            db.give_money(user, int(winnings))
            await interaction.response.send_message(embed=embed)
        else:
            db.take_money(user, bet)
            embed = Builder.basic_embed('Almost!, why not try again?').set_image(url='https://media1.tenor.com/m/kK8D7hQXX5wAAAAd/coins-tails.gif')
            await interaction.response.send_message(embed=embed)
    else:
        if prediction == 'tails':
            db.take_money(user, bet)
            winnings = str(bet + bet)
            embed = Builder.basic_embed('Congratulations! you win! ' + winnings + ' coins!'
                                        ).set_image(url='https://media1.tenor.com/m/kK8D7hQXX5wAAAAd/coins-tails.gif')
            db.give_money(user, int(winnings))
            await interaction.response.send_message(embed=embed)
        else:
            db.take_money(user, bet)
            embed = Builder.basic_embed('Almost!, why not try again?').set_image(
                url='https://sciencegems.wordpress.com/wp-content/uploads/2022/04/heads-coinflip.gif')

            await interaction.response.send_message(embed=embed)


@client.tree.command(name='roulette', description='A roulette command!')
@ensure_user_in_db()
async def roulette(interaction: discord.Interaction, bet: int, color: str = None, number: int = None):
    roulette_game = Roulette()
    user = interaction.user.id

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed('Insufficient balance!')
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed('Place a positive bet!')
        await interaction.response.send_message(embed=embed)
        return

    result, color_win = roulette_game.spin()
    db.give_money(user, -bet)
    if color and number:
        db.give_money(user, -bet)
        if (color == 'red' and number not in roulette_game.red_numbers) or \
                (color == 'black' and number not in roulette_game.black_numbers):
            await interaction.response.send_message(
                embed=Builder.basic_embed(f'Please choose compatible numbers!\n Red numbers: {", ".join(list(map(str, roulette_game.red_numbers)))}\n Black numbers: {", ".join(list(map(str, roulette_game.black_numbers)))}'))
            return

    if color == 'green':
        number = 0

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed('Insufficient balance!')
        await interaction.response.send_message(embed=embed)
        return

    if color is None and number is None:
        await interaction.response.send_message('You need at least one bet to play!')
        return

    if color is None and number:
        if result == number:
            db.give_money(user, bet * 35)
            embed = Builder.roulette_embed(win=True, number=result, color=color_win, winnings=bet * 35)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Builder.roulette_embed(win=False, number=result, color=color_win, winnings=None)
            await interaction.response.send_message(embed=embed)

    elif number is None and color:
        if color_win == color:
            db.give_money(user, bet * 2)
            embed = Builder.roulette_embed(win=True, number=result, color=color_win, winnings=bet * 2)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Builder.roulette_embed(win=False, number=result, color=color_win, winnings=None)
            await interaction.response.send_message(embed=embed)

    else:
        if color_win == color and result == number:
            db.give_money(user, bet * 35 * 2)
            embed = Builder.roulette_embed(win=True, number=result, color=color_win, winnings=bet * 35 * 2)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Builder.roulette_embed(win=False, number=result, color=color_win, winnings=None)
            await interaction.response.send_message(embed=embed)


@client.tree.command(name='list', description='List the available commands')
async def list_command(interaction: discord.Interaction):
    embed = Builder.basic_embed(

    """       
    
    <:1533takemymoney:1325913823533863014>   **/balance** - Shows your current coin balance.
    
    
    <:LeaderboardTrophy02:1209532891109916714> **/leaderboard** - Displays the leaderboard of the top players in the casino bot.
    
    
    🎲   **/guess** - Starts a number guessing game where you can win coins by guessing a number between 1 and 100.


    🃏   **/blackjack** - Play a game of Blackjack! Place a bet and try to beat the dealer.
    
    
    💸   **/free** - Gives you 250 coins if your balance is 0.
    
    
    🎰   **/slot** - Try your luck with the slot machine! Spin a 3x3 grid of symbols to win coins.
    
    
    📅   **/weekly** - Gives you 50,000 coins once a week.
    
    
    🎁   **/gift** - Gift coins to another user. You must have enough balance and the recipient must not be the bot.
    
    
    ℹ️   **/about** - Displays information about the bot and its creators.
    
    
    🪙   **/coinflip** - Flip a coin and try to predict if it will land on heads or tails.
    
    
    🎡   **/roulette** - Place a bet on a color or number in roulette and see if you win.
    
    
    """
                                )
    embed.title = 'Casino Bot Command List:'
    await interaction.response.send_message(embed=embed)


