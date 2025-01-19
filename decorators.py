import discord

from client import client
from dbconfig import DB
from src.builder import Builder
from src.translate import translate

db = DB()
import discord

def ensure_user_in_db():
    async def predicate(interaction: discord.Interaction):
        db.new_user(interaction.user.id)
        db.get_current_guild_language(interaction.guild.id)
        bot_member = interaction.guild.me
        channel = interaction.channel

        permissions = channel.permissions_for(bot_member)
        if not permissions.send_messages:
            embed = discord.Embed(
                title="Permission Error",
                description="I cannot send messages in this channel.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=bot_member.avatar.url)
            embed.add_field(name="Server", value=interaction.guild.name, inline=False)
            embed.add_field(name="Channel", value=f"<#{channel.id}>", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

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
            embed = Builder.basic_embed(desc=translate(key='place_positive_bet', guild_id=interaction.guild.id),guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)
            return

        return await func(interaction, *args, **kwargs)

    return wrapper

