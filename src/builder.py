import discord
from client import client

class Builder:

    @staticmethod
    def daily_embed(desc):
        return (
            discord.Embed(
                title="<:1013moneyz:1325913819335233609> Daily Reward!",
                description=desc,
                color=discord.Color.gold()
            )
            .set_thumbnail(
                url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/777-slots-handle-512.png"
            )
            .set_footer(
                text="Casino by The Cantina | Claim your reward daily!",
                icon_url=client.user.avatar.url if client.user.avatar else None
            )
        )

    @staticmethod
    def weekly_embed(desc):
        return (
            discord.Embed(
                title="<:1013moneyz:1325913819335233609> Weekly Reward!",
                description=desc,
                color=discord.Color.gold()
            )
            .set_thumbnail(
                url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/777-slots-handle-512.png"
            )
            .set_footer(
                text="Casino by The Cantina | Claim your reward daily!",
                icon_url=client.user.avatar.url if client.user.avatar else None
            )
        )

    @staticmethod
    def balance_embed(balance):
        return (
            discord.Embed(
                title=f'<:2063pokercoin:1325913832173993994> Your total balance is **{balance}**',
                color=discord.Color.gold()
            )
            .set_thumbnail(
                url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/777-slots-handle-512.png"
            )
            .set_footer(
                text="Casino by The Cantina | Claim your reward daily!",
                icon_url=client.user.avatar.url if client.user.avatar else None
            )
        )

    @staticmethod
    def create_leaderboard_embed(players, page):

        if not players:
            return discord.Embed(
                title='<:1013moneyz:1325913819335233609> Leaderboard',
                description="No players found for this page."
            )

        embed = discord.Embed(title='<:1013moneyz:1325913819335233609> Leaderboard')

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

                embed.set_footer(text='Page ' + str(page), icon_url=client.user.avatar)

        return embed

    @staticmethod
    def basic_embed(desc):
        return discord.Embed(
            title="<:1013moneyz:1325913819335233609> Casino",
            description=f'**{desc}**',
            color=discord.Color.gold()
        ).set_footer(
            text="Casino by The Cantina | Claim your reward daily!",
            icon_url=client.user.avatar.url
        )

    @staticmethod
    def roulette_embed(win, number, color, winnings):
        if color == 'black':
            color = '⚫'
        else:
            color = '🔴'

        embed_color = 0x4CAF50 if win else 0xFF0000
        embed = discord.Embed(
            title="<:1013moneyz:1325913819335233609> Casino",
            description="Here's the result of your roulette spin!",
            color=embed_color
        )

        embed.add_field(name="Spin Result", value=f"**Number**: {number}\n**Color**: {color}", inline=False)

        if win:
            embed.add_field(name="Congratulations!", value="You won your bet!", inline=False)
            embed.add_field(name='Winnings: ', value=winnings, inline=False)
        else:
            embed.add_field(name="Better Luck Next Time!", value="You lost your bet, try again!", inline=False)
        embed.set_footer(
            text="Casino by The Cantina | Claim your reward daily!",
            icon_url=client.user.avatar.url
        )

        return embed