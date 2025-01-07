import discord
from client import client

class Builder:
    # Static methods that will build the discord embeds for each command

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
                icon_url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/casino-chip-512.png"
            )
        )


    @staticmethod
    def basic_embed(desc):
        return discord.Embed(
            title="<:1013moneyz:1325913819335233609> Casino",
            description=f'**{desc}**',
            color=discord.Color.gold()
        ).set_footer(
            text="Casino by The Cantina | Claim your reward daily!",
            icon_url="https://cdn0.iconfinder.com/data/icons/sin-city-memories/128/casino-chip-512.png"
        )

    @staticmethod
    def balance_embed(balance):
        return discord.Embed(title='<:2063pokercoin:1325913832173993994> Your total balance is ' + f'**{balance}**').set_footer(text='Casino by The Cantina | Claim your reward daily!')

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

                embed.set_footer(text='Page ' + str(page))

        return embed

