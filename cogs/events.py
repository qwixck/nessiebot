import discord
from discord.ext import commands
import json
import os
import pymysql
import pymysql.cursors

class events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO `sets`(`id`) VALUES ({guild.id})")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM `sets` WHERE `id`={guild.id}")
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("assets/data/afks.json", "r") as f:
            data = json.load(f)
        for i in data:
            if f"{message.author.id}" in i:
                del data[f"{message.author.id}"]
                with open("assets/data/afks.json", "w") as f:
                    json.dump(data, f, indent=2)
                await message.channel.send(f"{message.author.mention}, I cleared your afk status!")
            if f"<@{i}>" in message.content:
                embed = discord.Embed(title = "AFK", color=discord.Color.embed_background(), description = f"<@{i}> is AFK ATM | Reason: `{data[f'{i}']['reason']}`")
                embed.set_thumbnail(url = "https://cdn3.emoji.gg/emojis/3929_idle.png")
                await message.channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("assets/data/friends.json", "r") as f:
            data = json.load(f)
        if member.guild.id == 702143845961433169:
            if member.id in data:
                channel = self.bot.get_channel(804364268858376272)
                await channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
                await member.send(f"Added you to <#804364268858376272>")
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT `welcomes` FROM `sets` WHERE `id`={member.guild.id}")
                result = cursor.fetchone()
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        channel = self.bot.get_channel(result["welcomes"])
        embed = discord.Embed(title = "Welcome!", description = f"{member.mention}. Welcome to **{member.guild.name}**. The amount of members in **{member.guild.name}** - `{member.guild.member_count}`", color=discord.Color.embed_background())
        embed.set_image(url=f"https://some-random-api.ml/welcome/img/1/night?type=join&username={member.name.replace(' ', '+')}&discriminator={member.discriminator}&guildName={member.guild.name.replace(' ', '+')}&memberCount={member.guild.member_count}&avatar={member.display_avatar}&textcolor=white&key={os.getenv('SOMERANDOMAPI_TOKEN')}")
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT `rooms_channel` FROM `sets` WHERE `id`={member.guild.id}")
                result = cursor.fetchone()
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        if after.channel != None:
            if after.channel.id == result["rooms_channel"]:
                if before.channel != None:
                    if before.channel.name == f"{member} room":
                            await delete(member)
                            await create(member)
                    else:
                        await create(member)
                else:
                    await create(member)
            if after.channel == None:
                if before.channel != None:
                    if before.channel.name == f"{member} room":
                            await delete(member)
            if after.channel.name != f"{member} room":
                if before.channel != None:
                    if before.channel.name == f"{member} room":
                            await delete(member)
        if after.channel == None:
            if before.channel.name == f"{member} room":
                await delete(member)
                
    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.errors.NotOwner):
            embed = discord.Embed(title = "Error", description = "This command is owner only", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.NotOwner(error)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = discord.Embed(title = "Error", description = f"I'm missing the following permission(s) to execute this command: {', '.join(error.missing_permissions)}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.BotMissingPermissions(error)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(title = "Error", description = f"You're missing the following permission(s) to execute this command: {', '.join(error.missing_permissions)}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.MissingPermissions(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title = "Error", description = f"You are missing the following argument to execute this command: `{error.param}`", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.MissingRequiredArgument(error)
        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = discord.Embed(title = "Error", description = f"Something went wrong while invoking this command", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.CommandInvokeError(error)
        elif isinstance(error, commands.errors.CommandOnCooldown):
            embed = discord.Embed(title = "Error", description = f"Cooldown is active. Try again in `{round(error.retry_after, 1)}` seconds", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.CommandOnCooldown(error)
        elif isinstance(error, commands.errors.MissingAnyRole):
            embed = discord.Embed(title = "Error", description = f"You are missing the following role(s): {error.missing_roles}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.MissingAnyRole(error)
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            embed = discord.Embed(title = "Error", description = "This command requires to be executed in a NSFW channel", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.NSFWChannelRequired(error)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(title = "Error", description = "Member wasn't found", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.send(file=file, embed=embed)
            raise commands.errors.MemberNotFound(error)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.errors.NotOwner):
            embed = discord.Embed(title = "Error", description = "This command is owner only", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.NotOwner(error)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = discord.Embed(title = "Error", description = f"I'm missing the following permission(s) to execute this command: {', '.join(error.missing_permissions)}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.BotMissingPermissions(error)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(title = "Error", description = f"You're missing the following permission(s) to execute this command: {', '.join(error.missing_permissions)}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.MissingPermissions(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title = "Error", description = f"You're missing the following argument to execute this command: `{error.param}`", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.MissingRequiredArgument(error)
        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = discord.Embed(title = "Error", description = f"Something went wrong while invoking this command", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.CommandInvokeError(error)
        elif isinstance(error, commands.errors.CommandOnCooldown):
            embed = discord.Embed(title = "Error", description = f"Cooldown is active. Try again in `{round(error.retry_after, 1)}` seconds", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.CommandOnCooldown(error)
        elif isinstance(error, commands.errors.MissingAnyRole):
            embed = discord.Embed(title = "Error", description = f"You're missing the following role(s): {error.missing_roles}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.MissingAnyRole(error)
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            embed = discord.Embed(title = "Error", description = "This command requires to be executed in a NSFW channel", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.NSFWChannelRequired(error)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(title = "Error", description = "Member wasn't found", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            embed.set_footer(text="If you believe this is not your mistake, please contact qwixck#3107")
            await ctx.respond(file=file, embed=embed)
            raise commands.errors.MemberNotFound(error)

def setup(bot):
    bot.add_cog(events(bot))

async def create(member: discord.Member):
    try:
        connection = pymysql.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT `rooms_category` FROM `sets` WHERE `id`={member.guild.id}")
                result = cursor.fetchone()
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    category = discord.utils.get(member.guild.categories, id=result["rooms_category"])
    channel = await member.guild.create_voice_channel(f"{member} room", category=category)
    await member.move_to(channel)
async def delete(member: discord.Member):
    channel = discord.utils.find(lambda c: c.name == f"{member} room", member.guild.channels)
    await channel.delete()