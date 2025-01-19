import discord
from dbconfig import DB
from src.builder import Builder

db = DB()

class LeaderboardButtons(discord.ui.View):
    def __init__(self, current_page, timeout=350):
        super().__init__(timeout=timeout)
        self.current_page = current_page

    @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.primary)
    async def previous_page_callback(self, interaction, button):
        total_pages = (db.db_length // 5) + (1 if db.db_length % 5 else 0)

        if self.current_page <= 1:
            self.current_page = total_pages
        else:
            self.current_page -= 1

        current_players = db.get_five_players(self.current_page)
        embed = Builder.create_leaderboard_embed(current_players, self.current_page, guild_id=interaction.guild.id)

        await interaction.response.edit_message(embed=embed, view=self)


    @discord.ui.button(label="Next Page", style=discord.ButtonStyle.primary)
    async def next_page_callback(self, interaction, button):
        total_pages = (db.db_length // 5) + (1 if db.db_length % 5 else 0)

        if self.current_page >= total_pages:
            self.current_page = 1
        else:
            self.current_page += 1

        current_players = db.get_five_players(self.current_page)
        embed = Builder.create_leaderboard_embed(current_players, self.current_page, guild_id=interaction.guild.id)

        await interaction.response.edit_message(embed=embed, view=self)
