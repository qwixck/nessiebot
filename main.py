import sys
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import pymysql
import pymysql.cursors

sys.setrecursionlimit(1500)
load_dotenv()
bot = commands.Bot(command_prefix=".", intents = discord.Intents.all(), help_command=None, case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.listening, name="/other bahelp"), status="online")

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Cog `{extension}` is loaded!")
    except:
        await ctx.send(f"Cog `{extension}` is undignified!")
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Cog `{extension}` is unloaded!")
    except:
        await ctx.send(f"Cog `{extension}` is undignified!")
@bot.command()
@commands.is_owner()
async def reload(ctx, extension = None):
    try:
        bot.load_extension(f"cogs.{extension}")
        bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Cog `{extension}` is reloaded!")
    except:
        await ctx.send(f"Cog `{extension}` is undignified!")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("DISCORD_TOKEN"))