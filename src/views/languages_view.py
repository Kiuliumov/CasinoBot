import discord
from dbconfig import DB

db = DB()

class LanguagesView(discord.ui.View):
    def __init__(self, timeout=350):
        super().__init__(timeout=timeout)

    @discord.ui.button(label='EN')
    async def en(self, interaction: discord.Interaction, button):
        db.change_current_guild_language(interaction.guild.id, 'en')
        await interaction.response.send_message('You now changed your server language to english!')

    @discord.ui.button(label='ES')
    async def es(self, interaction: discord.Interaction, button):
        db.change_current_guild_language(interaction.guild.id, 'es')
        await interaction.response.send_message('¡Ahora has cambiado el idioma de tu servidor a español!')

    @discord.ui.button(label='BG')
    async def bg(self, interaction: discord.Interaction, button):
        db.change_current_guild_language(interaction.guild.id, 'bg')
        await interaction.response.send_message('Вече смени езика на сървъра си на Български!')

    @discord.ui.button(label='DE')
    async def de(self, interaction: discord.Interaction, button):
        db.change_current_guild_language(interaction.guild.id, 'de')
        await interaction.response.send_message('Sie haben Ihre Serversprache bereits auf Deutsch umgestellt!')


