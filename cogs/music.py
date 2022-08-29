import discord
from discord.ext import commands
import youtube_dl
import asyncio
import os

youtube_dl.utils.bug_reports_message = lambda: ""
ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}
ffmpeg_options = {"options": "-vn"}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if "entries" in data:
            data = data["entries"][0]
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    music = discord.SlashCommandGroup("music", "Anything related to music!")

    @music.command(description="Plays a file from the local filesystem")
    @commands.is_owner()
    async def play(self, ctx: discord.ApplicationContext, query: str):
        if ctx.author.voice:
            if ctx.voice_client:
                pass
            else:
                await ctx.author.voice.channel.connect()
            if os.path.exists(f"assets/audio/{query}.mp3"):
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"assets/audio/{query}.mp3"))
                ctx.voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)
                await ctx.respond(f"Now playing: {query}")
            else:
                await ctx.respond("This file does not exists!")
        else:
            await ctx.respond("You need to be in VC!")

    @music.command(description="Plays from a url (almost anything youtube_dl supports)")
    @commands.is_owner()
    async def yt(self, ctx: discord.ApplicationContext, url: str):
        if ctx.author.voice:
            if ctx.voice_client:
                pass
            else:
                await ctx.author.voice.channel.connect()
            await ctx.defer()
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)
            await ctx.respond(f"Now playing: {player.title}")
        else:
            await ctx.respond("You need to be in VC!")

    @music.command(description="Changes the player's volume")
    @commands.is_owner()
    async def volume(self, ctx: discord.ApplicationContext, volume: discord.Option(int, min_value=0, max_value=100)):
        if ctx.author.voice:
            ctx.voice_client.source.volume = volume / 100
            await ctx.respond(f"Changed volume to {volume}%")
        else:
            await ctx.respond("You need to be in VC!")

    @music.command(description="Pauses player")
    @commands.is_owner()
    async def pause(self, ctx: discord.ApplicationContext):
        if ctx.author.voice:
            ctx.voice_client.pause()
            await ctx.respond("Paused player")
        else:
            await ctx.respond("You need to be in VC!")

    @music.command(description="Resume player")
    @commands.is_owner()
    async def resume(self, ctx: discord.ApplicationContext):
        if ctx.author.voice:
            ctx.voice_client.resume()
            await ctx.respond("Paused player")
        else:
            await ctx.respond("You need to be in VC!")

    @music.command(description="Stops and disconnects the bot from voice")
    @commands.is_owner()
    async def stop(self, ctx: discord.ApplicationContext):
        await ctx.voice_client.disconnect(force=True)
        await ctx.respond("Successfully disconnected from VC!")

def setup(bot):
    bot.add_cog(Music(bot))