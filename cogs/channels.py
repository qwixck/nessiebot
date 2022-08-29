import discord
from discord.ext import commands
from discord.commands import Option
import pymysql
import pymysql.cursors

class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    channels = discord.SlashCommandGroup("channels", "Anything related to channels")
    set = channels.create_subgroup("set", "Anything related to cmd set")

    @set.command(description="Get info about sets in server")
    @commands.guild_only()
    async def info(self, ctx: discord.ApplicationContext):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT `welcomes`, `logs`, `rooms_channel`, `rooms_category`, `tickets_opened_category`, `tickets_closed_category`, `tickets_admin`, `suggestions` FROM `sets` WHERE `id`={ctx.guild.id}")
                result = cursor.fetchone()
            connection.commit()
        except Exception as e:
                print(f"Error: {e}")
        embed = discord.Embed(title="Sets", color=discord.Color.embed_background())
        guild_icon = ctx.guild.icon.url if ctx.guild.icon else ""
        embed.set_thumbnail(url=guild_icon)
        embed.add_field(name="Welcomes", value=f"Channel: <#{result['welcomes']}>", inline=False)
        embed.add_field(name="Logs", value=f"Channel: <#{result['logs']}>", inline=False)
        embed.add_field(name="Rooms", value=f"Channel: <#{result['rooms_channel']}>\nCategory: <#{result['rooms_category']}>", inline=False)
        embed.add_field(name="Tickets", value=f"Opened category: <#{result['tickets_opened_category']}>\nClosed category: <#{result['tickets_closed_category']}>\nAdmin role: <@&{result['tickets_admin']}>", inline=False)
        embed.add_field(name="Suggestions", value=f"Channel: <#{result['suggestions']}>", inline=False)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(embed=embed)

    @set.command(description="Set welcomes")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def welcomes(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `sets` SET `welcomes`={channel.id} WHERE `id`={ctx.guild.id}")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        embed = discord.Embed(title="Succesfully changed", description=f"**Succesfully changed `welcomes` to {channel.mention}**", color=discord.Color.embed_background())
        file = discord.File("assets/images/success.png")
        embed.set_thumbnail(url="attachment://success.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file = file, embed=embed)

    @set.command(description="Set logs")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def logs(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `sets` SET `logs`={channel.id} WHERE `id`={ctx.guild.id}")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        embed = discord.Embed(title="Succesfully changed", description=f"**Succesfully changed `logs` to {channel.mention}**", color=discord.Color.embed_background())
        file = discord.File("assets/images/success.png")
        embed.set_thumbnail(url="attachment://success.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file = file, embed=embed)

    @set.command(description="Set rooms")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def rooms(self, ctx: discord.ApplicationContext, channel: discord.VoiceChannel, category: discord.CategoryChannel):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `sets` SET `rooms_channel`={channel.id}, `rooms_category`={category.id} WHERE `id`={ctx.guild.id}")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        embed = discord.Embed(title="Succesfully changed", description=f"**Succesfully changed `rooms channel` to {channel.mention} and `rooms category` to {category.mention}**", color=discord.Color.embed_background())
        file = discord.File("assets/images/success.png")
        embed.set_thumbnail(url="attachment://success.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file = file, embed=embed)

    @set.command(description="Set tickets")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def tickets(self, ctx: discord.ApplicationContext, opened_category: discord.CategoryChannel, closed_category: discord.CategoryChannel, admin: discord.Role):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `sets` SET `tickets_opened_category`={opened_category.id}, `tickets_closed_category`={closed_category.id}, `tickets_admin`={admin.id} WHERE `id`={ctx.guild.id}")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        embed = discord.Embed(title="Succesfully changed", description=f"**Succesfully changed `tickets opened_category` to {opened_category.mention} and `tickets closed_category` to {closed_category.mention} and `tickets admin` to {admin.mention}**", color=discord.Color.embed_background())
        file = discord.File("assets/images/success.png")
        embed.set_thumbnail(url="attachment://success.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file = file, embed=embed)

    @set.command(description="Set suggestions")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def suggestions(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE `sets` SET `suggestions`={channel.id} WHERE `id`={ctx.guild.id}")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        embed = discord.Embed(title="Succesfully changed", description=f"**Succesfully changed `suggestions` to {channel.mention}**", color=discord.Color.embed_background())
        file = discord.File("assets/images/success.png")
        embed.set_thumbnail(url="attachment://success.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.respond(file = file, embed=embed)

    @channels.command(description="Edit custom room's settings")
    @commands.guild_only()
    async def room(self, ctx: discord.ApplicationContext, type: Option(str, choices=["user_limit"]), setting: Option(int)):
        if ctx.author.voice == None:
            await ctx.respond("You need to be in voice channel!")
        elif ctx.author.voice.channel.name == f"{ctx.author} room":
            if type == "user_limit":
                channel = discord.utils.find(lambda c: c.name == f"{ctx.author} room", ctx.author.guild.channels)
                await ctx.respond(f"Changed <#{ctx.author.voice.channel.id}> {type} settings from `{ctx.author.voice.channel.user_limit}` to `{setting}`")
                await channel.edit(user_limit = int(setting))
        else:
            await ctx.respond("Only the creator of room can change room's settings!")

def setup(bot):
    bot.add_cog(Channels(bot))