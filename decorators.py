import discord
from dbconfig import DB
from src.builder import Builder

db = DB()
def ensure_user_in_db():
    async def predicate(interaction: discord.Interaction):
        db.new_user(interaction.user.id)
        return True
    return discord.app_commands.check(predicate)


def check_bet(func):
    async def wrapper(interaction: discord.Interaction, *args, **kwargs):
        bet_or_amount = None
        for param in kwargs.values():
            if isinstance(param, int) and param <= 0:
                bet_or_amount = param
                break

        if bet_or_amount is not None:
            embed = Builder.basic_embed("You must place a real bet!")
            await interaction.response.send_message(embed=embed)
            return

        return await func(interaction, *args, **kwargs)

    return wrapper
