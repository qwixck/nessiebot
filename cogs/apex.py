import os
import discord
from discord.ext import commands, pages
import aiohttp
from discord.commands import Option
import datetime

class Apex(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    apex = discord.SlashCommandGroup("apex", "Everything related to Apex Legends")

    @apex.command(description="Get the current map in rotations in Arenas and Battle Royale")
    async def map(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={os.getenv('APEX_TOKEN')}") as request:
                data = await request.json(content_type="utf-8")
        await session.close()
        try:
            embed = discord.Embed(title="Current Apex Legends map", color=discord.Color.embed_background())
            embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            embed.set_image(url=data['battle_royale']['current']['asset'])
            embed.add_field(name = "🗺 Battle Royale", value=f"Current **pubs** map is `{data['battle_royale']['current']['map']}`, ends <t:{data['battle_royale']['current']['end']}:t>.\nNext map is `{data['battle_royale']['next']['map']}` and will end <t:{data['battle_royale']['next']['end']}:t> (up to `{data['battle_royale']['next']['DurationInMinutes']}m`).\nCurrent **ranked** map is `{data['ranked']['current']['map']}`, ends <t:{data['ranked']['current']['end']}:d>.\nNext map is `{data['ranked']['next']['map']}`", inline=False)
            embed.add_field(name="⚔ Arenas", value=f"Current **pubs** map is `{data['arenas']['current']['map']}`, ends <t:{data['arenas']['current']['end']}:t>.\nNext map is `{data['arenas']['next']['map']}` and will end <t:{data['arenas']['next']['end']}:t> (up for `{data['arenas']['next']['DurationInMinutes']}m`).\nCurrent **ranked** map is `{data['arenasRanked']['current']['map']}`, ends <t:{data['arenasRanked']['current']['end']}:t>.\nNext map is `{data['arenasRanked']['next']['map']}` and will end <t:{data['arenasRanked']['next']['end']}:t> (up for `{data['arenasRanked']['next']['DurationInMinutes']}m`).", inline=False)
            await ctx.respond(embed = embed)
        except KeyError:
            await ctx.respond(data["Error"])

    @apex.command(name="server-status", description="Get current Apex Legends servers status")
    async def server_status(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mozambiquehe.re/servers?auth={os.getenv('APEX_TOKEN')}") as request:
                data = await request.json(content_type="utf-8")
        await session.close()
        try:
            embed = discord.Embed(title="Current Apex Legends servers", color=discord.Color.embed_background())
            embed.set_thumbnail(url="https://logos-world.net/wp-content/uploads/2020/11/Apex-Legends-Emblem.png")
            embed.add_field(name="Origin Login", value=f"🇪🇺 EU West is {data['Origin_login']['EU-West']['Status']}\n🇪🇺 EU East is {data['Origin_login']['EU-East']['Status']}\n🇺🇸 US West is {data['Origin_login']['US-West']['Status']}\n🇺🇸 US Central is {data['Origin_login']['US-Central']['Status']}\n🇺🇸 US East is {data['Origin_login']['US-East']['Status']}\n🇧🇷 South America is {data['Origin_login']['SouthAmerica']['Status']}\n🇯🇵 Asia is {data['Origin_login']['Asia']['Status']}")
            embed.add_field(name="EA Novafusion", value=f"🇪🇺 EU West is {data['EA_novafusion']['EU-West']['Status']}\n🇪🇺 EU East is {data['EA_novafusion']['EU-East']['Status']}\n🇺🇸 US West is {data['EA_novafusion']['US-West']['Status']}\n🇺🇸 US Central is {data['EA_novafusion']['US-Central']['Status']}\n🇺🇸 US East is {data['EA_novafusion']['US-East']['Status']}\n🇧🇷 South America is {data['EA_novafusion']['SouthAmerica']['Status']}\n🇯🇵 Asia is {data['EA_novafusion']['Asia']['Status']}")
            embed.add_field(name="EA Accounts", value=f"🇪🇺 EU West is {data['EA_accounts']['EU-West']['Status']}\n🇪🇺 EU East is {data['EA_accounts']['EU-East']['Status']}\n🇺🇸 US West is {data['EA_accounts']['US-West']['Status']}\n🇺🇸 US Central is {data['EA_accounts']['US-Central']['Status']}\n🇺🇸 US East is {data['EA_accounts']['US-East']['Status']}\n🇧🇷 South America is {data['EA_accounts']['SouthAmerica']['Status']}\n🇯🇵 Asia is {data['EA_accounts']['Asia']['Status']}")
            embed.add_field(name="ApexOauth Crossplay", value=f"🇪🇺 EU West is {data['ApexOauth_Crossplay']['EU-West']['Status']}\n🇪🇺 EU East is {data['ApexOauth_Crossplay']['EU-East']['Status']}\n🇺🇸 US West is {data['ApexOauth_Crossplay']['US-West']['Status']}\n🇺🇸 US Central is {data['ApexOauth_Crossplay']['US-Central']['Status']}\n🇺🇸 US East is {data['ApexOauth_Crossplay']['US-East']['Status']}\n🇧🇷 South America is {data['ApexOauth_Crossplay']['SouthAmerica']['Status']}\n🇯🇵 Asia is {data['ApexOauth_Crossplay']['Asia']['Status']}")
            embed.add_field(name="ALS services", value=f"Status website is {data['selfCoreTest']['Status-website']['Status']}\nStats API is {data['selfCoreTest']['Stats-API']['Status']}\nOverflow #1 is {data['selfCoreTest']['Overflow-#1']['Status']}\nOverflow #2 is {data['selfCoreTest']['Overflow-#2']['Status']}\nOrigin API is {data['selfCoreTest']['Origin-API']['Status']}\n<:PS4:956613742735544360> Playstation API is {data['selfCoreTest']['Playstation-API']['Status']}\n<:XB1:943071432294948904> Xbox API is {data['selfCoreTest']['Xbox-API']['Status']}")
            embed.add_field(name="Other Platforms", value=f"<:PS4:956613742735544360> Playstation Network is {data['otherPlatforms']['Playstation-Network']['Status']}\n<:XB1:943071432294948904> Xbox Live is {data['otherPlatforms']['Xbox-Live']['Status']}")
            embed.set_footer(text="More data & Report your issues on apexlegendsstatus.com")
            await ctx.respond(embed = embed)
        except KeyError:
            await ctx.respond(data["Error"])

    @apex.command(description="Get a player statistics")
    async def stats(self, ctx: discord.ApplicationContext, platform: Option(str, "Choose platform", choices=["PC", "XB1", "PS4"]), type: Option(str, "Choose type", choices=["nickname", "uid"]), player: str, legend: Option(str, "Choose legend", choices=["Ash", "Bangalore", "Bloodhound", "Caustic", "Crypto", "Fuse", "Gibraltar", "Horizon", "Lifeline", "Loba", "Mad Maggie", "Mirage", "Octane", "Pathfinder", "Rampart", "Revenant", "Seer", "Valkyrie", "Wattson", "Wraith"], required = False)):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            if type == "nickname":
                async with session.get(f"https://api.mozambiquehe.re/bridge?platform={platform}&player={player}&auth={os.getenv('APEX_TOKEN')}&enableClubsBeta") as request:
                    data = await request.json(content_type="utf-8")
            else:
                async with session.get(f"https://api.mozambiquehe.re/bridge?platform={platform}&uid={player}&auth={os.getenv('APEX_TOKEN')}&enableClubsBeta") as request:
                    data = await request.json(content_type="utf-8")
        await session.close()
        try:
            if data['realtime']['isOnline'] == 1:
                lobby = "🟢 Online"
            else:
                lobby = "🔴 Offline or unknown status"
        except KeyError:
            await ctx.respond(data["Error"])
        try:
            if data["global"]["name"] == "":
                name = "INVALID CHATACTERS"
            else:
                name = data["global"]["name"]
        except KeyError:
            await ctx.respond(data["Error"])
        else:
            if legend == None:
                try:
                    embed = discord.Embed(title=f"{name}'s stats", url=f"https://apexlegendsstatus.com/profile/uid/{platform}/{data['global']['uid']}", description=lobby, color=discord.Color.embed_background())
                    embed.set_thumbnail(url=str(data["club"]["logo"]))
                    embed.add_field(name="⚙ General", value=f"Level `{data['global']['level']}`\nBP level `{data['global']['battlepass']['level']} ({data['global']['toNextLevelPercent']}%)`")
                    embed.add_field(name="👑 Ranked", value=f"**BR** {data['global']['rank']['rankName']}, `{data['global']['rank']['rankScore']}` RP\n**Arena** {data['global']['arena']['rankName']}, `{data['global']['arena']['rankScore']}` AP")
                    embed.add_field(name=f"Club \"{data['club']['name']}\"", value=f"ID `{data['club']['id']}`\nTag `{data['club']['tag']}`\nCreated by UID `{data['club']['createdByUID']}`\nGroup size `{data['club']['groupSize']}`\nMax group size `{data['club']['maxGroupSize']}`\nDatacenter `{data['club']['datacenter']}`\nIs free to join `{data['club']['joinConfig']['isFreeJoin']}`", inline=False)
                    embed.set_footer(text = f"Incorrect data? Select the trackers in-game and try again. To update your BP level, select the BP badge in game. Want to see more stats? Click on {name}'s stats at the top of this message")
                    await ctx.respond(embed = embed)
                except KeyError:
                    await ctx.respond(data["Error"])
            else:
                try:
                    if data["legends"]["selected"]["LegendName"] == legend:
                        embed = discord.Embed(title=f"{name}'s {legend}'s stats", url=f"https://apexlegendsstatus.com/profile/uid/{platform}/{data['global']['uid']}", description=lobby, color=discord.Color.embed_background())
                        embed.set_image(url=data['legends']['selected']['ImgAssets']['banner'])
                        embed.set_thumbnail(url=data["global"]["rank"]["rankImg"])
                        embed.add_field(name="⚙ General", value=f"Level `{data['global']['level']}`\nBP level `{data['global']['battlepass']['level']} ({data['global']['toNextLevelPercent']}%)`")
                        embed.add_field(name="👑 Ranked", value=f"**BR** {data['global']['rank']['rankName']}, `{data['global']['rank']['rankScore']}` RP\n**Arena** {data['global']['arena']['rankName']}, `{data['global']['arena']['rankScore']}` AP")
                        embed.add_field(name="Equipment", value=f"**🥋 Skin** `{data['legends']['selected']['gameInfo']['skin']}`\n**🖼 Frame** `{data['legends']['selected']['gameInfo']['frame']}`\n**🤺 Pose** `{data['legends']['selected']['gameInfo']['pose']}`\n**😀 Intro** `\"{data['legends']['selected']['gameInfo']['intro']}\"`", inline=False)
                        for i in data["legends"]["selected"]["data"]:
                            embed.add_field(name=i["name"], value=f"Value `{i['value']}`", inline=False)
                        embed.set_footer(text = f"Incorrect data? Select the trackers in-game and try again. To update your BP level, select the BP badge in game. Want to see more stats? Click on {name}'s {legend}'s stats at the top of this message")
                        await ctx.respond(embed = embed)
                    else:
                        embed = discord.Embed(title=f"{name}'s {legend}'s stats", url=f"https://apexlegendsstatus.com/profile/uid/{platform}/{data['global']['uid']}", description=lobby, color=discord.Color.embed_background())
                        embed.set_image(url=data['legends']['all'][legend]['ImgAssets']['banner'])
                        embed.set_thumbnail(url=data["global"]["rank"]["rankImg"])
                        embed.add_field(name="⚙ General", value=f"Level `{data['global']['level']}`\nBP level `{data['global']['battlepass']['level']} ({data['global']['toNextLevelPercent']}%)`")
                        embed.add_field(name="👑 Ranked", value=f"**BR** {data['global']['rank']['rankName']}, `{data['global']['rank']['rankScore']}` RP\n**Arena** {data['global']['arena']['rankName']}, `{data['global']['arena']['rankScore']}` AP")
                        for i in data["legends"]["all"][legend]["data"]:
                            embed.add_field(name=i["name"], value=f"Value `{i['value']}`", inline=False)
                        embed.set_footer(text = f"Incorrect data? Select the trackers in-game and try again. To update your BP level, select the BP badge in game. Want to see more stats? Click on {name}'s {legend}'s stats at the top of this message")
                        await ctx.respond(embed = embed)
                except KeyError:
                    await ctx.respond(data["Error"])

    @apex.command(description="View current Apex Legends shop")
    async def shop(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mozambiquehe.re/store?auth={os.getenv('APEX_TOKEN')}") as request:
                data = await request.json()
        await session.close()
        list = []
        for i in range(0, len(data)):
            list.append(discord.Embed(title = "Shop", color=discord.Color.embed_background()))
            if len(data[i]["content"]) == 1:
                if len(data[i]["pricing"]) == 1:
                    list[i].add_field(name = data[i]["title"], value = f"**Content**\n{data[i]['content'][0]['name']}, quantity `{data[i]['content'][0]['quantity']}`\n**Price**\n{data[i]['pricing'][0]['ref']} `{data[i]['pricing'][0]['quantity']}`\n**Expire time** <t:{data[i]['expireTimestamp']}>\n**OfferID** `{data[0]['offerID']}`")
                else:
                    list[i].add_field(name = data[i]["title"], value = f"**Content**\n{data[i]['content'][0]['name']}, quantity `{data[i]['content'][0]['quantity']}`\n**Price**\n{data[i]['pricing'][0]['ref']} `{data[i]['pricing'][0]['quantity']}`\n{data[i]['pricing'][1]['ref']} `{data[i]['pricing'][1]['quantity']}`\n**Expire time** <t:{data[i]['expireTimestamp']}>\n**OfferID** `{data[0]['offerID']}`")
            if len(data[i]["content"]) == 2:
                if len(data[i]["pricing"]) == 1:
                    list[i].add_field(name = data[i]["title"], value = f"**Content**\n{data[i]['content'][0]['name']}, quantity `{data[i]['content'][0]['quantity']}`\n{data[i]['content'][1]['name']}, quantity `{data[i]['content'][1]['quantity']}`\n**Price**\n{data[i]['pricing'][0]['ref']} `{data[i]['pricing'][0]['quantity']}`\n**Expire time** <t:{data[i]['expireTimestamp']}>\n**OfferID** `{data[0]['offerID']}`")
                else:
                    list[i].add_field(name = data[i]["title"], value = f"**Content**\n{data[i]['content'][0]['name']}, quantity `{data[i]['content'][0]['quantity']}`\n{data[i]['content'][1]['name']}, quantity `{data[i]['content'][1]['quantity']}`\n**Price**\n{data[i]['pricing'][0]['ref']} `{data[i]['pricing'][0]['quantity']}`\n{data[i]['pricing'][1]['ref']} `{data[i]['pricing'][1]['quantity']}`\n**Expire time** <t:{data[i]['expireTimestamp']}>\n**OfferID** `{data[0]['offerID']}`")
            if len(data[i]["content"]) == 3:
                if len(data[i]["pricing"]) == 1:
                    list[i].add_field(name = data[i]["title"], value = f"**Content**\n{data[i]['content'][0]['name']}, quantity `{data[i]['content'][0]['quantity']}`\n{data[i]['content'][1]['name']}, quantity `{data[i]['content'][1]['quantity']}`\n{data[i]['content'][2]['name']}, quantity `{data[i]['content'][2]['quantity']}`\n**Price**\n{data[i]['pricing'][0]['ref']} `{data[i]['pricing'][0]['quantity']}`\n**Expire time** <t:{data[i]['expireTimestamp']}>\n**OfferID** `{data[0]['offerID']}`")
                else:
                    list[i].add_field(name = data[i]["title"], value = f"**Content**\n{data[i]['content'][0]['name']}, quantity `{data[i]['content'][0]['quantity']}`\n{data[i]['content'][1]['name']}, quantity `{data[i]['content'][1]['quantity']}`\n{data[i]['content'][2]['name']}, quantity `{data[i]['content'][2]['quantity']}`\n**Price**\n{data[i]['pricing'][0]['ref']} `{data[i]['pricing'][0]['quantity']}`\n{data[i]['pricing'][1]['ref']} `{data[i]['pricing'][1]['quantity']}`\n**Expire time** <t:{data[i]['expireTimestamp']}>\n**OfferID** `{data[0]['offerID']}`")
            list[i].set_image(url = data[i]["asset"])
            list[i].set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await pages.Paginator(list, timeout=None).respond(ctx.interaction)

    @apex.command(description="See how many points you need to reach Apex Predator on each platform")
    async def predator(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mozambiquehe.re/predator?auth={os.getenv('APEX_TOKEN')}") as request:
                data = await request.json(content_type=None)
        await session.close()
        try:
            embed = discord.Embed(title="How many points to reach Apex Predator?", color=discord.Color.embed_background())
            embed.set_author(name="Click to view charts", url="https://apexlegendsstatus.com/points-for-predator")
            embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            embed.add_field(name="<:predator:956613743301775441> Battle Royale", value=f"`{data['RP']['PC']['val']}` on PC <:PC:956613741678579772>\n`{data['RP']['PS4']['val']}` on PS4 <:PS4:956613742735544360>\n`{data['RP']['X1']['val']}` on XB1 <:XB1:956613742941057044>\n`{data['RP']['SWITCH']['val']}` on Switch <:Switch:956613742290952262>\n")
            embed.add_field(name="<:predator:956613743301775441> Arenas", value=f"`{data['AP']['PC']['val']}` on PC <:PC:956613741678579772>\n`{data['AP']['PS4']['val']}` on PS4 <:PS4:956613742735544360>\n`{data['AP']['X1']['val']}` on XB1 <:XB1:956613742941057044>\n`{data['AP']['SWITCH']['val']}` on Switch <:Switch:956613742290952262>\n")
            await ctx.respond(embed = embed)
        except KeyError:
            await ctx.respond(data['Error'])

    @apex.command(description = "Get latest news")
    async def news(self, ctx: discord.ApplicationContext, language: Option(str, "select language", choices = ["en-US", "ru", "fr", "it", "pl", "es"], required=True)):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mozambiquehe.re/news?auth={os.getenv('APEX_TOKEN')}&lang={language}") as request:
                data = await request.json(content_type = None)
        await session.close()
        list = []
        for i in range(0, len(data)):
            list.append(discord.Embed(title = data[i]["title"], description = data[i]["short_desc"], url = data[i]["link"], color=discord.Color.embed_background()))
            list[i].set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            list[i].set_image(url = data[i]["img"])
        await pages.Paginator(list, timeout=None).respond(ctx.interaction)

    @apex.command(description = "What you can craft right now in replicator?")
    async def crafting(self, ctx):
        await ctx.defer()
        """async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mozambiquehe.re/crafting?auth={os.getenv('APEX_TOKEN')}") as request:
                data = await request.json(content_type=None)
        await session.close()
        class colors:
            common = 128, 128, 128
            rare = 0, 148, 255
            epic = 178, 0, 255
            legendary = 0, 0, 0
        list = []
        for a in range(0, len(data)):
            for b in range(0, len(data[a]["bundleContent"])):
                if data[a]['bundleContent'][b]['itemType']['rarity'] == "Common":
                    color = colors().common
                if data[a]['bundleContent'][b]['itemType']['rarity'] == "Rare":
                    color = colors().rare
                if data[a]['bundleContent'][b]['itemType']['rarity'] == "Epic":
                    color = colors().epic
                if data[a]['bundleContent'][b]['itemType']['rarity'] == "Legendary":
                    color = colors().legendary
            list.append(discord.Embed(title = "Crafting", color = discord.Color.from_rgb(color[0], color[1], color[2])))
            for b in range(0, len(data[a]["bundleContent"])):
                list[a].add_field(name = data[a]["bundleContent"][b]['itemType']["name"], value = f"Bundle type `{data[a]['bundleType']}`\nPrice `{data[a]['bundleContent'][b]['cost']}`", inline = False)
                list[a].set_thumbnail(url = data[a]['bundleContent'][b]['itemType']['asset'])
        await pages.Paginator(list, timeout=None).respond(ctx.interaction)"""
        await ctx.respond("In maintaince, someday it will end...", ephemeral=True)

    @apex.command(description="Display time till new season")
    async def season(self, ctx: discord.ApplicationContext):
        date = datetime.datetime(2022, 8, 9, 20, 0, 0, 0) - datetime.datetime.now()
        embed = discord.Embed(title=f"Time until new season: {date}", description="<t:1660064400>", color=discord.Color.embed_background())
        embed.set_image(url="https://apexlegendsstatus.com/assets/apex-s14-cd.png?s14prod")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Apex(bot))