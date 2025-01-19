import asyncio

from dbconfig import DB
import discord
from discord.ext import commands

from src.blackjack import Blackjack
from src.builder import Builder
from client import client
from src.translate import translate
from src.views.game_views import BlackjackView
from src.views.languages_view import LanguagesView
from src.views.leaderboard_page import LeaderboardButtons
from decorators import ensure_user_in_db
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
        error_message = translate("daily_error", interaction.guild_id)
        embed = Builder.daily_embed(error_message, interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    embed = Builder.daily_embed(desc=None, title=translate("daily_success", interaction.guild_id), guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed)


@daily.error
async def on_test_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)

        time = f"{hours}:{minutes}:{seconds}"
        cooldown_message = translate("daily_cooldown", guild_id=interaction.guild.id, time=time)
        embed = Builder.daily_embed(cooldown_message, interaction.guild.id, title=translate("daily_error", interaction.guild_id))
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='balance', description="Returns your balance")
@ensure_user_in_db()
async def balance(interaction: discord.Interaction):
    user_id = interaction.user.id
    balance = db.get_balance(user_id)
    embed = Builder.balance_embed(str(balance), guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='leaderboard', description='The leaderboard of all players in the casino bot!')
@ensure_user_in_db()
async def leaderboard(interaction: discord.Interaction):
    current_page = 1
    current_players = db.get_five_players(current_page)
    embed = Builder.create_leaderboard_embed(current_players, current_page, guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed, view=LeaderboardButtons(current_page))


@client.tree.command(name='guess', description='A number guessing game')
@ensure_user_in_db()
async def guess_the_number(interaction: discord.Interaction, bet: int):
    user = interaction.user.id
    user_balance = db.get_balance(user)

    if user_balance < bet:
        embed = Builder.basic_embed(desc= translate(key='insufficient_balance', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed(translate(key='place_positive_bet', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    db.take_money(user, bet)

    import random
    secret_number = random.randint(1, 100)
    tries = 5

    embed = Builder.basic_embed(desc=translate(key='guess_intro', guild_id=interaction.guild.id, tries=tries), guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed)

    def check(message):
        return message.author == interaction.user and message.channel == interaction.channel

    while tries > 0:
        try:
            message = await client.wait_for('message', check=check, timeout=30.0)
            guess = int(message.content)

            if guess == secret_number:
                winnings = bet * 1 + tries
                db.give_money(user, winnings)
                embed = Builder.basic_embed(translate(key='guess_correct', guild_id=interaction.guild.id, number=secret_number, winnings=winnings), guild_id=interaction.guild.id)
                await interaction.followup.send(embed=embed)
                return
            elif guess < secret_number:
                feedback = translate(key='guess_feedback_too_low', guild_id=interaction.guild.id)
            else:
                feedback = translate(key='guess_feedback_too_high', guild_id=interaction.guild.id)

            tries -= 1
            if tries != 0:
                embed = Builder.basic_embed(translate(key='guess_wrong', guild_id=interaction.guild.id, feedback=feedback, tries=tries), guild_id=interaction.guild.id)
                await interaction.followup.send(embed=embed)
        except ValueError:
            await interaction.followup.send('Enter a valid number!')
        except asyncio.TimeoutError:
            embed = Builder.basic_embed(translate(key='guess_timeout', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
            await interaction.followup.send(embed=embed)
            return

    embed = Builder.basic_embed(translate(key='guess_game_over', guild_id=interaction.guild.id, number=secret_number),
                                guild_id=interaction.guild.id)
    await interaction.followup.send(embed=embed)


@client.tree.command(name="blackjack", description="Play a game of Blackjack")
@ensure_user_in_db()
async def blackjack(interaction: discord.Interaction, bet: int):
    user = interaction.user.id
    user_balance = db.get_balance(user)

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed(desc=translate(key='insufficient_balance', guild_id=interaction.guild.id),
                                    guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed(desc=translate(key='place_positive_bet', guild_id=interaction.guild.id),
                                    guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    game = Blackjack()
    game.start_game(bet, user_balance)

    player_hand_str = game.get_hand_string(game.player_hand)
    dealer_hand_str = f"{game.dealer_hand[0]}, ?"

    embed = Builder.basic_embed(
        f"{translate(key='blackjack_intro', bet=bet, balance=user_balance, guild_id=interaction.guild.id)}\n\n"
        f"{translate(key='blackjack_your_hand', guild_id=interaction.guild.id)} `: {player_hand_str}`\n {translate(key='blackjack_dealer_hand', guild_id=interaction.guild.id)} `: {dealer_hand_str}`\n\n",
        guild_id=interaction.guild.id).set_image(url='https://i.postimg.cc/1tXDDWnP/output.jpg')

    view = BlackjackView(game, interaction, bet, user)
    await interaction.response.send_message(embed=embed, view=view)


@client.tree.command(name="free", description="Gives you free coins if you're amount is 0")
@ensure_user_in_db()
async def free(interaction: discord.Interaction):
    user = interaction.user
    if db.get_balance(user.id) == 0:
        db.give_money(user.id, 250)
        embed = Builder.basic_embed(translate(key='free_success', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
    embed = Builder.basic_embed(translate(key='free_rich', guild_id=interaction.guild.id),
                                guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='slot', description='A slot machine')
@ensure_user_in_db()
async def slot(interaction: discord.Interaction):
    embed = discord.Embed(title='Welcome to slots!',
                          description=translate(key='slot_intro', guild_id=interaction.guild.id)).set_thumbnail(
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
        embed = Builder.basic_embed(desc=translate('daily_error', interaction.guild_id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    embed = Builder.weekly_embed(desc=translate('weekly_success', interaction.guild_id), guild_id=interaction.guild.id)
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

        embed = Builder.daily_embed(desc=translate('daily_cooldown', interaction.guild_id, time=time_message), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='gift', description='Gift money to a user')
@ensure_user_in_db()
async def gift(interaction: discord.Interaction, amount: int, user: discord.User):
    user_id = interaction.user.id

    if not db.check_if_user_is_registered(user.id):
        db.new_user(user.id)

    if user.id == user_id:
        # Translate the error message
        await interaction.response.send_message(translate('gift_self_error', interaction.guild_id))
        return

    user_balance = db.get_balance(user_id)
    if user.id == client.user.id:
        await interaction.response.send_message(translate('gift_bot_error', interaction.guild_id))
        return

    if amount > user_balance:
        embed = Builder.basic_embed(translate('gift_insufficient', interaction.guild_id))
        await interaction.response.send_message(embed=embed)
        return

    db.give_money(user.id, amount)
    db.take_money(user_id, amount)

    embed = Builder.basic_embed(translate('gift_success', interaction.guild_id, giver=interaction.user.display_name, amount=amount, receiver=user.display_name), guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='about', description='Information about the bot')
@ensure_user_in_db()
async def about(interaction: discord.Interaction):
    embed = discord.Embed(title=translate('about', interaction.guild_id)).set_author(name=f'{client.user.name}', icon_url=client.user.avatar)
    embed.description = translate('about', interaction.guild_id)
    embed.set_image(url='https://img.freepik.com/free-vector/golden-casino-background-with-playing-cards_1017-33699.jpg')
    embed.set_footer(text=translate('footer', interaction.guild_id))
    await interaction.response.send_message(embed=embed)

@client.tree.command(name='coinflip', description='A coinflip command!')
@ensure_user_in_db()
async def coinflip(interaction: discord.Interaction, bet: int, prediction: str):
    if prediction != 'heads' and prediction != 'tails':
        embed = Builder.basic_embed(desc=translate(key='coinflip_invalid_prediction', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    user = interaction.user.id

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed(desc=translate(key='insufficient_balance', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed(translate('place_positive_bet', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    computer_choice = random.randint(0, 1)
    if computer_choice == 0:
        computer_choice = 'tails'
    else:
        computer_choice = 'heads'

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed(desc=translate(key='insufficient_balance', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    if computer_choice == 'heads':
        if prediction == 'heads':
            db.take_money(user, bet)
            winnings = str(bet + bet)
            embed = Builder.basic_embed(translate(key='coinflip_win', guild_id=interaction.guild.id, winnings=winnings), guild_id=interaction.guild.id
                                        ).set_image(url='https://sciencegems.wordpress.com/wp-content/uploads/2022/04/heads-coinflip.gif')
            db.give_money(user, int(winnings))
            await interaction.response.send_message(embed=embed)
        else:
            db.take_money(user, bet)
            embed = Builder.basic_embed(translate(key='coinflip_lose', guild_id=interaction.guild.id), guild_id=interaction.guild.id).set_image(url='https://sciencegems.wordpress.com/wp-content/uploads/2022/04/heads-coinflip.gif')
            await interaction.response.send_message(embed=embed)
    else:
        if prediction == 'tails':
            db.take_money(user, bet)
            winnings = str(bet + bet)
            embed = Builder.basic_embed(translate(key='coinflip_win', guild_id=interaction.guild.id, winnings=winnings), guild_id=interaction.guild.id
                                        ).set_image(url='https://media1.tenor.com/m/kK8D7hQXX5wAAAAd/coins-tails.gif')
            db.give_money(user, int(winnings))
            await interaction.response.send_message(embed=embed)
        else:
            db.take_money(user, bet)
            embed = Builder.basic_embed(translate(key='coinflip_lose', guild_id=interaction.guild.id), guild_id=interaction.guild.id).set_image(
                url='https://media1.tenor.com/m/kK8D7hQXX5wAAAAd/coins-tails.gif')

            await interaction.response.send_message(embed=embed)


@client.tree.command(name='roulette', description='A roulette command!')
@ensure_user_in_db()
async def roulette(interaction: discord.Interaction, bet: int, color: str = None, number: int = None):
    guild_id = interaction.guild.id
    roulette_game = Roulette()
    user = interaction.user.id

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed(desc= translate(key='insufficient_balance', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    if bet <= 0:
        embed = Builder.basic_embed(desc=translate('place_positive_bet', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return
    if ((color == 'red' and (number is not None and number not in roulette_game.red_numbers)) or
            (color == 'black' and (number is not None and number not in roulette_game.black_numbers)) or
            (color not in ['green', 'red', 'black']) or
            (number is not None and not (0 <= number <= 36))):
        await interaction.response.send_message(
            embed=Builder.basic_embed(
                f'{translate(key="roulette_invalid", guild_id=guild_id)}\n 🔴 {", ".join(list(map(str, roulette_game.red_numbers)))}\n\n ⚫ {", ".join(list(map(str, roulette_game.black_numbers)))}',
                guild_id=guild_id))
        return

    result, color_win = roulette_game.spin()
    if color and number:
        db.give_money(user, -bet)


    if color == 'green':
        number = 0

    if db.get_balance(user) < bet:
        embed = Builder.basic_embed(translate(key='insufficient_balance', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)
        return

    if color is None and number is None:
        await interaction.response.send_message(translate(key="roulette_invalid", guild_id=guild_id))
        return

    if color is None and number:
        if result == number:
            db.give_money(user, bet * 35)
            embed = Builder.roulette_embed(win=True, number=result, color=color_win, winnings=bet * 35, guild_id=guild_id)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Builder.roulette_embed(win=False, number=result, color=color_win, winnings=None, guild_id=guild_id)
            await interaction.response.send_message(embed=embed)

    elif number is None and color:
        if color_win == color:
            db.give_money(user, bet * 2)
            embed = Builder.roulette_embed(win=True, number=result, color=color_win, winnings=bet * 2, guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Builder.roulette_embed(win=False, number=result, color=color_win, winnings=None, guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)

    else:
        if color_win == color and result == number:
            db.give_money(user, bet * 35 * 2)
            embed = Builder.roulette_embed(win=True, number=result, color=color_win, winnings=bet * 35 * 2, guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Builder.roulette_embed(win=False, number=result, color=color_win, winnings=None, guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)


@client.tree.command(name='list', description='List the available commands')
@ensure_user_in_db()
async def list_command(interaction: discord.Interaction):
    embed = Builder.basic_embed(desc=translate(key='command_list', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='setlanguage', description='Change your server language. Requires administrator privileges')
@ensure_user_in_db()
async def setlanguage(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        embed = Builder.basic_embed(desc=translate(key='user_permissions_error', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed)

    else:
        embed = Builder.basic_embed(desc=translate(key='language_message', guild_id=interaction.guild.id), guild_id=interaction.guild.id)
        available_languages = translate(key='get_all', guild_id=interaction.guild.id)
        for language in available_languages.keys():
            embed.add_field(name=f'`{language}` ----> {available_languages[language]['language_text']}', value='', inline='false')
        await interaction.response.send_message(embed=embed, view=LanguagesView())


@client.tree.command(name='vote', description='Vote for the discord bot')
@ensure_user_in_db()
async def vote(interaction: discord.Interaction):

        embed = Builder.basic_embed(desc='Vote for Casino now!', guild_id=interaction.guild.id)
        await interaction.response.send_message(embed=embed, view=discord)


client.run('')
