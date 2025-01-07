import discord
from dbconfig import DB

db = DB()
def ensure_user_in_db():
    async def predicate(interaction: discord.Interaction):
        db.new_user(interaction.user.id)
        return True
    return discord.app_commands.check(predicate)