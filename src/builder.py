import discord
from client import client
from src.translate import translate


class Builder:

    @staticmethod
    def daily_embed(desc, guild_id, title):
        return (
            discord.Embed(
                title=f"<:1013moneyz:1325913819335233609> {title}",
                description=desc,
                color=discord.Color.gold()
            )
            .set_thumbnail(
                url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/777-slots-handle-512.png"
            )
            .set_footer(
                text=translate(key='footer',guild_id=guild_id),
                icon_url=client.user.avatar.url if client.user.avatar else None
            )
        )

    @staticmethod
    def weekly_embed(desc, guild_id):
        return (
            discord.Embed(
                title=f"<:1013moneyz:1325913819335233609> {translate('weekly_success', guild_id)}",
                description=desc,
                color=discord.Color.gold()
            )
            .set_thumbnail(
                url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/777-slots-handle-512.png"
            )
            .set_footer(
                text=translate(key='footer', guild_id=guild_id),
                icon_url=client.user.avatar.url if client.user.avatar else None
            )
        )

    @staticmethod
    def balance_embed(balance, guild_id):
        return (
            discord.Embed(
                title=translate('balance', guild_id, balance=balance),
                color=discord.Color.gold()
            )
            .set_thumbnail(
                url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/777-slots-handle-512.png"
            )
            .set_footer(
                text=translate(key='footer', guild_id=guild_id),
                icon_url=client.user.avatar.url if client.user.avatar else None
            )
        )

    @staticmethod
    def create_leaderboard_embed(players, page, guild_id):
        if not players:
            return discord.Embed(
                title=f"<:1013moneyz:1325913819335233609> {translate('leaderboard_title', guild_id)}",
                description="No players found for this page."
            )

        embed = discord.Embed(title=f"<:1013moneyz:1325913819335233609> {translate('leaderboard_title', guild_id)}")

        user = client.get_user(players[0][0])
        avatar_url = user.avatar
        embed.set_thumbnail(url=avatar_url)

        for idx, player in enumerate(players, start=(page - 1) * 5 + 1):
            user = client.get_user(player[0])
            if user:
                player_info = f"**{user.name}** - {player[1]} coins <:2063pokercoin:1325913832173993994>"

                embed.add_field(
                    name=f'',
                    value=f'**#{idx}** ----------> {player_info}\n',
                    inline=False
                )

                embed.set_footer(text=f"Page {page}", icon_url=client.user.avatar)

        return embed

    @staticmethod
    def basic_embed(desc, guild_id):
        return discord.Embed(
            title=f"<:1013moneyz:1325913819335233609> Casino",
            description=f'**{desc}**',
            color=discord.Color.gold()
        ).set_footer(
            text=translate(key='footer', guild_id=guild_id),
            icon_url=client.user.avatar.url
        )

    @staticmethod
    def roulette_embed(win, number, color, winnings, guild_id):
        if color == 'black':
            color = '⚫'
        else:
            color = '🔴'

        embed_color = 0x4CAF50 if win else 0xFF0000
        embed = discord.Embed(
            title=f"<:1013moneyz:1325913819335233609> Casino",
            description=translate('roulette_win' if win else 'roulette_lose', guild_id, number=number, color=color, winnings=winnings),
            color=embed_color
        )

        embed.set_footer(
            text=translate(key='footer', guild_id=guild_id),
            icon_url=client.user.avatar.url
        )

        return embed
