import discord
from discord.ext import commands, pages
from discord.commands import Option
import aiohttp

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    valorant = discord.SlashCommandGroup("valorant", "Everything related to Valorant")

    @valorant.command(description="Get latest match history")
    async def match(self, ctx: discord.ApplicationContext, name: str, tag: str, region: Option(str, choices=["eu", "na", "kr", "ap"])):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{name.replace(' ', '+')}/{tag}") as request:
                data = await request.json()
        await session.close()
        if data["status"] != 200:
            await ctx.respond(f"Error: {data['message']}")
        else:
            list = []
            for i in range(0, 5):
                list.append(discord.Embed(title=data["data"][i]["metadata"]["map"],description=f"Red has won: {data['data'][i]['teams']['red']['has_won']}\nBlue has won: {data['data'][i]['teams']['blue']['has_won']}" , color=discord.Color.embed_background()))
                list[i].add_field(name="Data", value=f"Mode `{data['data'][i]['metadata']['mode']}`", inline=False)
                for a in data["data"][i]["players"]["all_players"]:
                    list[i].add_field(name=a["name"], value=f"Team: `{a['team']}`\nCharacter: `{a['character']}`\nKills: `{a['stats']['kills']}`\nDeaths: `{a['stats']['deaths']}`\nAssists: `{a['stats']['assists']}`")
                list[i].set_thumbnail(url="https://logos-download.com/wp-content/uploads/2021/01/Valorant_Logo.png")
                list[i].set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            await pages.Paginator(list, timeout=None).respond(ctx.interaction)

    @valorant.command(description="Get latest Valorant news")
    async def news(self, ctx: discord.ApplicationContext, lang: Option(str, choices=["en-us", "en-gb", "de-de", "es-es", "es-mx", "fr-fr", "it-it", "ja-jp", "ko-kr", "pt-br", "ru-ru", "tr-tr", "vi-vn"])):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v1/website/{lang}") as request:
                data = await request.json()
        await session.close()
        if data["status"] != 200:
            await ctx.respond(f"Error: {data['message']}")
        else:
            list = []
            for i in range(0, 30):
                list.append(discord.Embed(title=data["data"][i]["title"], description=data["data"][i]["category"], url=data["data"][i]["url"], color=discord.Color.embed_background()))
                list[i].set_image(url=data["data"][i]["banner_url"])
                list[i].add_field(name="External link", value=f"[Click here!]({data['data'][i]['external_link']})")
                list[i].set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            await pages.Paginator(list, timeout=None).respond(ctx.interaction)

    @valorant.command(description="Get account information")
    async def account(self, ctx: discord.ApplicationContext, name: str, tag: str, region: Option(str, choices=["ap", "br", "eu", "kr", "latam", "na"])):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name.replace(' ', '+')}/{tag}?force=true") as request:
                data = await request.json()
            async with session.get(f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name.replace(' ', '+')}/{tag}") as request2:
                data2 = await request2.json()
        await session.close()
        if data["status"] != 200:
            await ctx.respond(f"Error: {data['message']}")
        if data2["status"] != 200:
            await ctx.respond(f"Error: {data2['message']}")
        else:
            embed = discord.Embed(title=f"{name}#{tag}", color=discord.Color.embed_background())
            embed.set_image(url=data["data"]["card"]["wide"])
            embed.add_field(name="Data", value=f"Account lvl: `{data['data']['account_level']}`\nPUUID: `{data['data']['puuid']}`\nCurrent tier: `{data2['data']['current_data']['currenttierpatched']}`\nELO change to last game: `{data2['data']['current_data']['mmr_change_to_last_game']}`\nELO: `{data2['data']['current_data']['elo']}`")
            embed.set_footer(text=f"Old: {data2['data']['current_data']['old']}")
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Valorant(bot))