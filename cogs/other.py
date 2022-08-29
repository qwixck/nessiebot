import discord
from discord.ext import commands
from discord.commands import Option
import aiohttp
import io
import json
import random
import asyncio
import os
import datetime
import random
import pymysql
import pymysql.cursors


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    other = discord.SlashCommandGroup("other", "Anything related to other")

    @other.command(description="Help")
    async def bahelp(self, ctx: discord.ApplicationContext):
        class Embed(discord.Embed):
            def __init__(self2) -> None:
                super().__init__(title = "Bahelp", description="Commands info", color=discord.Color.embed_background())
                self2.set_author(name=self.bot.user, icon_url=self.bot.user.display_avatar)
                self2.set_thumbnail(url=self.bot.user.display_avatar)
                self2.set_footer(icon_url=ctx.author.display_avatar, text=f"Requested by: {ctx.author}")
        class Select(discord.ui.Select):
            def __init__(self3) -> None:
                super().__init__(placeholder = "Commands")
                self3.add_option(label="Mod", description="Get moderation commands", emoji="🛡️", value="moderation")
                self3.add_option(label="Apex Legends", description="Get Apex Legends commands", emoji="🎮", value="apex")
                self3.add_option(label="Valorant", description="Get Valorant commnds", emoji="🎮", value="valorant")
                self3.add_option(label="Channels", description="Get channels commands", emoji="📝", value="channels")
                self3.add_option(label="Other", description="Get other commands", emoji="⚙️", value="other")
                self3.add_option(label="Ticket", description="Get ticket commands", emoji="✉", value="ticket")
                async def select_callback(interaction):
                    embed = Embed()
                    if interaction.user != ctx.author:
                        await interaction.response.send_message("You can't do that!", ephemeral = True)
                    if self3.values[0] == "moderation":
                        embed.add_field(name="</mod kick:1004101976096780411>", value="> Kick member from server")
                        embed.add_field(name="</mod ban:1004101976096780411>", value="> Bans member from server")
                        embed.add_field(name="</mod clear:1004101976096780411>", value="> Purge set amount of message")
                        embed.add_field(name=".ticket", value="> Sends a ticket message")
                        embed.add_field(name="</mod log:1004101976096780411>", value="> Save chat in html file")
                        embed.add_field(name="</mod stfu:1004101976096780411>", value="> Shuts the fuck up member")
                        embed.add_field(name="</mod warn:1004101976096780411>", value="> Warns member. If member has 3 warns - auto ban")
                        embed.add_field(name="</mod warns:1004101976096780411>", value="> Get member's info about warns he have")
                        embed.add_field(name="</mod removewarns:1004101976096780411>", value="> Removes all warns from member")
                        await interaction.response.edit_message(embed=embed)
                    if self3.values[0] == "apex":
                        embed.add_field(name="</apex crafting:1001556323739115552>", value="> What you can craft right now in replicator?")
                        embed.add_field(name="</apex map:1001556323739115552>", value="> Get the current map rotations in Arenas and Battle Royale")
                        embed.add_field(name="</apex news:1001556323739115552>", value="> Get latest news")
                        embed.add_field(name="</apex predator:1001556323739115552>", value="> See how many poinst you need to reach Apex Predator on each platform")
                        embed.add_field(name="</apex server-status:1001556323739115552>", value="> Get current servers status")
                        embed.add_field(name="</apex shop:1001556323739115552>", value="View current shop")
                        embed.add_field(name="`</apex stats:1001556323739115552>", value="Get a player's statitics")
                        await interaction.response.edit_message(embed = embed)
                    if self3.values[0] == "valorant":
                        embed.add_field(name="</valorant match:1001556323739115551>", value="> Get latest match history")
                        embed.add_field(name="</valorant account:1001556323739115551>", value="> Get account info")
                        embed.add_field(name="</valorant news:1001556323739115551>", value="Get latest news")
                        await interaction.response.edit_message(embed=embed)
                    if self3.values[0] == "channels":
                        embed.add_field(name="`/set ...`", value="> Set channels, categories and roles")
                        embed.add_field(name="</channels room:1004101976096780409>", value="> Change customs room's settings")
                        await interaction.response.edit_message(embed = embed)
                    if self3.values[0] == "other":
                        embed.add_field(name="</other bahelp:1004101976096780410>", value="> That's where are you right now")
                        embed.add_field(name="</other ping:1004101976096780410>", value="> Get bot's current ping")
                        embed.add_field(name="</other rock:1004101976096780410>", value="> 🤨")
                        embed.add_field(name="</other capybara:1004101976096780410>", value=" > Get a capybara image")
                        embed.add_field(name="</other minipig:1004101976096780410>", value="> Get a minipig image")
                        embed.add_field(name="</other about:1004101976096780410>", value="> Get information about __member__")
                        embed.add_field(name="`.say`", value="> Bot will send your message")
                        embed.add_field(name="`</other flirt:1004101976096780410>", value="> 😏")
                        embed.add_field(name="</other hug:1004101976096780410>", value="> You hug member")
                        embed.add_field(name="</other kick_ass:1004101976096780410>", value="> You kick member's ass")
                        embed.add_field(name="</other afk:1004101976096780410>", value="> Set custom afk")
                        embed.add_field(name="</other nitro:1004101976096780410>", value="100% free nitro no scam without registration and bobux deposit")
                        embed.add_field(name="</other avatar:1004101976096780410>", value="> Get member's avatar")
                        embed.add_field(name="</other overlay:1004101976096780410>", value="> Customize member's avatar")
                        embed.add_field(name="</other stupid:1004101976096780410>", value="> Generates meme \"Stupid Dog\" with member's avatar")
                        embed.add_field(name="</other simp:1004101976096780410>", value="> Generates meme \"Simp\" with member's avatar")
                        embed.add_field(name="</other lied:1004101976096780410>", value="> Generates meme \"Lied\" with member's avatar")
                        embed.add_field(name="</other amogus:1004101976096780410>", value="> Generates meme \"Among Us\" with member's avatar")
                        embed.add_field(name="</other pet:1004101976096780410>", value="> Pet member")
                        embed.add_field(name="</other genshin:1004101976096780410>", value="> Genshin Impact card")
                        embed.add_field(name="</other amogus:1004101976096780410>", value="> Generates meme \"Among Us\" with member's avatar")
                        embed.add_field(name="</other tweet:1004101976096780410>", value="> Fake tweet")
                        embed.add_field(name="</other comment:1004101976096780410>", value="> Faske YouTube comment")
                        embed.add_field(name="</other suggest:1004101976096780410>", value="> Suggest things to server! (If available!)")
                        embed.add_field(name="</other nobitches:1004101976096780410>", value="> Generates meme \"Among Us\" with member's avatar")
                        await interaction.response.edit_message(embed = embed)
                    if self3.values[0] == "ticket":
                        embed.add_field(name="</ticket close:1004101976096780412>", value="> Close ticket")
                        embed.add_field(name="</ticket delete:1004101976096780412>", value="> Delete ticket")
                        embed.add_field(name="</ticket transcript:1004101976096780412>", value="> Save channel messages in HTML file")
                        await interaction.response.edit_message(embed=embed)
                self3.callback = select_callback
        view = discord.ui.View(timeout=None)
        view.add_item(Select())
        await ctx.respond(embed=Embed(), view=view)

    @other.command(description="Get bot's ping")
    async def ping(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Pong!", description=f"⏳: {round(self.bot.latency * 1000)}ms", color=discord.Color.embed_background())
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed=embed)

    @other.command(description="Random 🤨")
    @commands.cooldown(rate = 1, per = 5.0)
    async def rock(self, ctx: discord.ApplicationContext):
        luckyrock = random.randint(1, 10)
        embed = discord.Embed(title="Loading rock...", color=discord.Color.embed_background())
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed=embed)
        async with aiohttp.ClientSession() as session:
            if luckyrock == 1:
                async with session.get("http://api.qwixck.lol/rock/video") as request:
                    file = discord.File(io.BytesIO(await request.read()), "rock.mp4")
                await session.close()
                await ctx.interaction.edit_original_message("lucky boy", file=file, embed=None)
            if luckyrock != 1:
                async with session.get("http://api.qwixck.lol/rock/gif") as request:
                    file = discord.File(io.BytesIO(await request.read()), "rock.gif")
                await session.close()
                embed = discord.Embed(title="Rock", color=discord.Color.embed_background())
                embed.set_image(url="attachment://rock.gif")
                embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.interaction.edit_original_message(file=file, embed=embed)

    @other.command(description="Random capy")
    @commands.cooldown(rate = 1, per = 5.0)
    async def capybara(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Loading image...", color=discord.Color.embed_background())
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        async with aiohttp.ClientSession() as session:
            await ctx.respond(embed=embed)
            async with session.get("http://api.qwixck.lol/capybara/image") as img:
                file = discord.File(io.BytesIO(await img.read()), "capybara.png")
        await session.close()
        embed = discord.Embed(title="Capybara", color=discord.Color.embed_background())
        embed.set_image(url="attachment://capybara.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.interaction.edit_original_message(file=file, embed=embed)

    @other.command(description="Random minipig")
    @commands.cooldown(rate = 1, per = 5.0)
    async def minipig(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Loading image...", color=discord.Color.embed_background())
        await ctx.respond(embed = embed)
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.qwixck.lol/minipig/image") as img:
                file = discord.File(io.BytesIO(await img.read()), "minipig.png")
        await session.close()
        embed = discord.Embed(title = "Minipig", color=discord.Color.embed_background())
        embed.set_image(url = "attachment://minipig.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.interaction.edit_original_message(file = file, embed = embed)

    @other.command(description="Get info about member")
    @commands.guild_only()
    async def about(self, ctx: discord.ApplicationContext, member: Option(discord.Member, required=False)):
        if member == None:
            member = ctx.author
        rlist = []
        for role in member.roles:
            rlist.append(role.mention)
        b = ", ".join(rlist)
        embed = discord.Embed(color=discord.Color.embed_background())
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        embed.set_author(name=member, icon_url=member.display_avatar)
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="About", value=f"{member.mention} | id: `{member.id}`")
        date_format = "%m/%d/%Y, %H:%M:%S" 
        embed.add_field(name="Joined", value=f"{member.joined_at.strftime(date_format)}", inline=False)
        embed.add_field(name="Registered", value=f"{member.created_at.strftime(date_format)}", inline=False)
        embed.add_field(name='Bot?', value=member.bot, inline=False)
        embed.add_field(name=f'Roles:({len(rlist)})', value=''.join([b]),inline=False)
        embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)
        await ctx.respond(embed=embed)

    @other.command(description="Flirt with member")
    async def flirt(self, ctx: discord.ApplicationContext, member: discord.Member):
        embed = discord.Embed(title = "sussy baka", description=f"{member.mention}, {ctx.author.mention} wants to flirt with you", color=discord.Color.embed_background())
        embed.set_image(url = "https://birgerritzenhoff.at/among-us-twerk.gif")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed = embed)

    @other.command(description="Hug member")
    async def hug(self, ctx: discord.ApplicationContext, member: discord.Member):
        embed = discord.Embed(title = "Hug", color=discord.Color.embed_background(), description = f"{member.mention}, {ctx.author.mention} wants to hug you")
        embed.set_image(url = "https://i.kym-cdn.com/photos/images/original/002/080/148/94c.jpg")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed = embed)

    @other.command(description="Kick member's ass")
    async def kick_ass(self, ctx: discord.ApplicationContext, member: discord.Member):
        embed = discord.Embed(title = "Kick ass", color=discord.Color.embed_background(), description = f"{member.mention}, {ctx.author.mention} wants to kick your ass")
        embed.set_image(url = "https://image.shutterstock.com/image-photo/full-length-photo-handsome-guy-260nw-1559830010.jpg")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed = embed)

    @other.command(description="Set custom AFK")
    async def afk(self, ctx: discord.ApplicationContext, type: Option(str, choices=["set"]), reason: Option(str, required=False)):
        if type == "set":
            with open("assets/data/afks.json", "r") as f:
                data = json.load(f)
            data[f"{ctx.author.id}"] = {}
            data[f"{ctx.author.id}"]["reason"] = reason
            await asyncio.sleep(1)
            with open("assets/data/afks.json", "w") as f:
                json.dump(data, f, indent=2)
            embed = discord.Embed(title = "Succesfully set afk", description = f"{ctx.author.mention} set afk | Reason: `{reason}`", color=discord.Color.embed_background())
            file = discord.File("assets/images/success.png")
            embed.set_thumbnail(url="attachment://success.png")
            embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            await ctx.respond(file=file, embed=embed)

    @other.command(description="100% free nitro no scam without registration and bobux deposit")
    async def nitro(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(description=f"{ctx.author.mention} generated nitro link!", color=discord.Color.embed_background())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        button = discord.ui.Button(label="Claim", emoji="🌈", style=discord.ButtonStyle.green)
        async def callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You can't do that!", ephemeral=True)
            else:
                await interaction.response.send_message("https://imgur.com/NQinKJB", ephemeral=True)
                embed = discord.Embed(description=f"{ctx.author.mention} claimed the nitro!", color=discord.Color.embed_background())
                embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
                embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                button2 = discord.ui.Button(label="Claimed", emoji="🌈", style=discord.ButtonStyle.red, disabled=True)
                view = discord.ui.View(timeout=None)
                view.add_item(button2)
                await ctx.interaction.edit_original_message(embed=embed, view=view)
        button.callback = callback
        view = discord.ui.View(timeout=None)
        view.add_item(button)
        await ctx.respond(embed=embed, view=view)

    @other.command(description="Get member's avatar")
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member):
        embed = discord.Embed(title=f"{member.name}'s avatar", color=discord.Color.embed_background(), url=member.display_avatar)
        embed.set_image(url=member.display_avatar)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed=embed)

    @other.command(description="Customize member's avatar")
    async def overlay(self, ctx: discord.ApplicationContext, member: discord.Member, type: Option(str, choices=["gay", "glass", "wanted", "passed", "jail", "comrade", "triggered"])):
        if type == "gay" or "glass" or "wanted" or "passed" or "jail" or "comrade":
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://some-random-api.ml/canvas/{type}?avatar={member.display_avatar}") as imgData:
                    file = discord.File(io.BytesIO(await imgData.read()), f"{member.name}-{type}.png")
            await session.close()
            embed = discord.Embed(title=f"{member.name} {type}", color=discord.Color.embed_background())
            embed.set_image(url=f"attachment://{member.name}-{type}.png")
            embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            await ctx.respond(file=file, embed=embed)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://some-random-api.ml/canvas/{type}?avatar={member.display_avatar}") as imgData:
                    file = discord.File(io.BytesIO(await imgData.read()), f"{member.name.replace(' ', '_')}-{type}.gif")
            await session.close()
            embed = discord.Embed(title=f"{member.name} {type}", color=discord.Color.embed_background())
            embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-{type}.gif")
            embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            await ctx.respond(file=file, embed=embed)

    @other.command(description="Stupid meme")
    async def stupid(self, ctx: discord.ApplicationContext, member: discord.Member, content: str):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/canvas/its-so-stupid?avatar={member.display_avatar}&dog={content}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-stupid.png")
        await session.close()
        embed = discord.Embed(title=f"Stupid", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-stupid.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Simp card")
    async def simp(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/canvas/simpcard?avatar={member.display_avatar}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-simpcard.png")
        await session.close()
        embed = discord.Embed(title=f"Simp card", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-simpcard.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="idk what to type here")
    async def lied(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/canvas/lied?avatar={member.display_avatar}&username={member.name}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-lied.png")
        await session.close()
        embed = discord.Embed(title=f"Lied", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-lied.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Is he imposter?")
    async def amogus(self, ctx: discord.ApplicationContext, member: discord.Member, imposter: Option(str, choices=["true", "false"])):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/premium/amongus?avatar={member.display_avatar}&username={member.name}&imposter={imposter}&key={os.getenv('SOMERANDOMAPI_TOKEN')}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-amogus.gif")
        await session.close()
        embed = discord.Embed(title="Amogus", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-amogus.gif")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Pet member")
    async def pet(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/premium/petpet?avatar={member.display_avatar}&key={os.getenv('SOMERANDOMAPI_TOKEN')}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-pet.gif")
        await session.close()
        embed = discord.Embed(title=f"Pet", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-pet.gif")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Genshin Impact card")
    async def genshin(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            member_created_at = member.created_at.date()
            async with session.get(f"https://some-random-api.ml/canvas/namecard?avatar={member.display_avatar}&birthday={member_created_at}&username={member.name}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-genshin.png")
        await session.close()
        embed = discord.Embed(title=f"Genshin card", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-genshin.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Fake tweet")
    async def tweet(self, ctx: discord.ApplicationContext, member: discord.Member, content: str):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            nick = member.nick
            if nick == None:
                nick = member.name
            async with session.get(f"https://some-random-api.ml/canvas/tweet?avatar={member.display_avatar}&comment={content.replace(' ', '+')}&username={member.name}&displayname={nick.replace(' ', '+')}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-tweet.png")
        await session.close()
        embed = discord.Embed(title=f"Tweet", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-tweet.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Fake youtube comment")
    async def comment(self, ctx: discord.ApplicationContext, member: discord.Member, content: str):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            nick = member.nick
            if nick == None:
                nick = member.name.replace(" ", "+")
            async with session.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={member.display_avatar}&comment={content.replace(' ', '+')}&username={nick}") as request:
                file = discord.File(io.BytesIO(await request.read()), f"{member.name.replace(' ', '_')}-comment.png")
        await session.close()
        embed = discord.Embed(title=f"Youtube comment", color=discord.Color.embed_background())
        embed.set_image(url=f"attachment://{member.name.replace(' ', '_')}-comment.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Suggest things to server! (If available)")
    @commands.guild_only()
    async def suggest(self, ctx: discord.ApplicationContext, image: Option(str, "only images url", required = False)):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT `suggestions` FROM `sets` WHERE `id`={ctx.guild.id}")
                result = cursor.fetchone()
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        if result["suggestions"] == None:
            await ctx.interaction.response.send_message("Sorry, the suggestions aren't available atm!", ephemeral = True)
        else:
            channel = self.bot.get_channel(result["suggestions"])
            class MyModal(discord.ui.Modal):
                def __init__(self) -> None:
                    super().__init__(title = "Suggestion")
                    self.add_item(discord.ui.InputText(
                        label = "Title", 
                        placeholder="Enter title", 
                        max_length = 256
                    ))
                    self.add_item(discord.ui.InputText(
                        label = "Suggestion",
                        placeholder = "Type your suggestion!",
                        style = discord.InputTextStyle.long,
                        max_length = 1024
                    ))
                async def callback(self, interaction: discord.Interaction):
                    embed = discord.Embed(title = "Suggestion", color=discord.Color.embed_background(), timestamp=datetime.datetime.now())
                    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                    embed.set_image(url = image)
                    embed.add_field(name = self.children[0].value, value=self.children[1].value, inline = False)
                    try:
                        message = await channel.send(embed = embed)
                    except discord.errors.HTTPException:
                        embed.remove_image()
                        message = await channel.send(embed = embed)
                    await message.add_reaction("✅")
                    await message.add_reaction("❌")
                    await interaction.response.send_message("Your suggestion has been sent!", ephemeral = True)
            await ctx.interaction.response.send_modal(MyModal())

    @other.command(description="\"No bitches?\" custom meme")
    async def nobitches(self, ctx: discord.ApplicationContext, text: str):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://some-random-api.ml/canvas/nobitches?no={text.replace(' ', '+')}") as request:
                file = discord.File(io.BytesIO(await request.read()), "nobitches.png")
        await session.close()
        embed = discord.Embed(title="No bitches?", color=discord.Color.embed_background())
        embed.set_image(url="attachment://nobitches.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file=file, embed=embed)

    @other.command(description="Sends your image to a random member of server")
    async def ranimage(self, ctx: discord.ApplicationContext, image: discord.Attachment):
        if str(image.content_type) != "image/png":
            await ctx.respond("Invalid format!", ephemeral=True)
        else:
            member = random.choice(ctx.guild.members)
            while member.bot != False:
                member = random.choice(ctx.guild.members)
            try:
                await member.send(f"{ctx.author} used </other ranimage:1000457656865140889> on you\nServer: {ctx.guild}", file=await image.to_file(spoiler=True))
                await ctx.respond(f"Success!\nYour file was sent to: {member}", ephemeral=True)
            except:
                await ctx.respond("Member have turned off his DMs, try again", ephemeral=True)

def setup(bot):
    bot.add_cog(Other(bot))