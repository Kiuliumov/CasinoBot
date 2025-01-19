import discord
from dbconfig import DB
from src.builder import Builder
from src.translate import translate

db = DB()

class LanguagesView(discord.ui.View):
    def __init__(self, timeout=350):
        super().__init__(timeout=timeout)

    @discord.ui.button(label='EN')
    async def en(self, interaction: discord.Interaction, button):
        if not interaction.user.guild_permissions.administrator:
            embed = Builder.basic_embed(desc=translate(key='user_permissions_error', guild_id=interaction.guild.id),
                                        guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)

        db.change_current_guild_language(interaction.guild.id, 'en')
        await interaction.response.send_message('You now changed your server language to english!')

    @discord.ui.button(label='ES')
    async def es(self, interaction: discord.Interaction, button):

        if not interaction.user.guild_permissions.administrator:
            embed = Builder.basic_embed(desc=translate(key='user_permissions_error', guild_id=interaction.guild.id),
                                        guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)

        db.change_current_guild_language(interaction.guild.id, 'es')
        await interaction.response.send_message('¡Ahora has cambiado el idioma de tu servidor a español!')

    @discord.ui.button(label='BG')
    async def bg(self, interaction: discord.Interaction, button):

        if not interaction.user.guild_permissions.administrator:
            embed = Builder.basic_embed(desc=translate(key='user_permissions_error', guild_id=interaction.guild.id),
                                        guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)

        db.change_current_guild_language(interaction.guild.id, 'bg')
        await interaction.response.send_message('Вече смени езика на сървъра си на Български!')

    @discord.ui.button(label='DE')
    async def de(self, interaction: discord.Interaction, button):

        if not interaction.user.guild_permissions.administrator:
            embed = Builder.basic_embed(desc=translate(key='user_permissions_error', guild_id=interaction.guild.id),
                                        guild_id=interaction.guild.id)
            await interaction.response.send_message(embed=embed)

        db.change_current_guild_language(interaction.guild.id, 'de')
        await interaction.response.send_message('Sie haben Ihre Serversprache bereits auf Deutsch umgestellt!')


