import discord
from discord.ext import commands
from discord.commands import Option
import json
import datetime
import chat_exporter
import io
from utils.banandkicked import BanAndKicked
import pymysql
import pymysql.cursors

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    mod = discord.SlashCommandGroup("mod", "Anytning related to moderation")

    @mod.command(description="Kick member from server")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: discord.ApplicationContext, member:discord.Member, reason: Option(str, required=False) = None):
        if member.guild_permissions.administrator:
            await ctx.respond("You can't kick admin!")
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT `logs` FROM `sets` WHERE `id`={ctx.guild.id}")
                    result = cursor.fetchone()
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
            channel = self.bot.get_channel(result["logs"])
            member_data = member
            await ctx.guild.kick(member, reason=reason)
            await BanAndKicked().Chat(ctx, member_data, reason).kicked()
            if channel != None:
                await BanAndKicked().Mod(ctx, channel, member_data, reason).kicked()

    @mod.command(description="Ban member from server")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason: Option(str, required=False) = None):
        if member.guild_permissions.administrator:
            await ctx.respond("You can't ban admin!")
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT `logs` FROM `sets` WHERE `id`={ctx.guild.id}")
                    result = cursor.fetchone()
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
            channel = self.bot.get_channel(result["logs"])
            member_data = member
            await ctx.guild.ban(member, reason=reason)
            await BanAndKicked().Chat(ctx, member_data, reason).banned()
            if channel != None:
                await BanAndKicked().Mod(ctx, channel, member_data, reason).banned()

    @mod.command(description="Purdge set amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: discord.ApplicationContext, amount: discord.Option(int, max_value=1000)):
        confirm = discord.ui.Button(style=discord.ButtonStyle.danger, label="Confirm",)
        cancel = discord.ui.Button(style=discord.ButtonStyle.grey, label="Cancel")
        async def confirm_button(interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You can't do that!", ephemeral=True)
            else:
                await ctx.channel.purge(limit=amount + 1)
        async def cancel_button(interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You can't do that!", ephemeral=True)
            else:
                await message.delete()
        view = discord.ui.View(timeout=None)
        confirm.callback = confirm_button
        cancel.callback = cancel_button
        view.add_item(confirm)
        view.add_item(cancel)
        message = await ctx.respond(f"Are you sure that you want to delete `{amount}` messages?", view=view)

    @mod.command(description="Save chat in html file")
    async def log(self, ctx: discord.ApplicationContext, limit: discord.Option(int, max_value=1000), tz_info: Option(str, choices=["UTC"])):
        transcript = await chat_exporter.export(ctx.channel, limit=limit, tz_info=tz_info,)
        if transcript is None:
            return
        transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html",)
        await ctx.respond(file=transcript_file)

    @mod.command(description="Mutes member")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def stfu(self, ctx: discord.ApplicationContext, member: discord.Member, time: int):
        if member.guild_permissions.administrator:
            await ctx.respond("You can't mute admin!")
        else:
            duration = datetime.timedelta(minutes=time)
            await member.timeout_for(duration, reason="didn't stfu")
            await ctx.respond(f"{member.mention} \"stfu pls\" - Ciupcik")

    @mod.command(description="Warns user")
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx: discord.ApplicationContext, member: discord.Member, reason: Option(str, required=False)):
        with open("assets/data/warns.json", "r") as f:
            data = json.load(f)
        if member.guild_permissions.administrator:
            await ctx.respond("You can\'t warn admin!")
            return
        if not ctx.guild.id in data:
            data = str(ctx.guild.id)
        if not f"{member.id}" in data[f"{member.guild.id}"]:
            data[f"{member.guild.id}"][f"{member.id}"] = {}
            data[f"{member.guild.id}"][f"{member.id}"]["count"] = 1
            data[f"{member.guild.id}"][f"{member.id}"]["warns"] = []
            data[f"{member.guild.id}"][f"{member.id}"]["warns"].append({
                "moderator": {
                    "full_name": f"{ctx.author}",
                    "id": ctx.author.id
                },
                "reason": reason
            })
            embed = discord.Embed(title = "Succesfully warned", description = f"{member} was successfully warned! | Reason: `{reason}`", color=discord.Color.embed_background())
            embed.set_thumbnail(url = "https://cdn.picpng.com/check_mark/check-mark-tick-mark-check-63841.png")
            await ctx.respond(embed = embed)
        else:
            data[f"{member.guild.id}"][f"{member.id}"]["count"] += 1
            data[f"{member.guild.id}"][f"{member.id}"]["warns"].append({
                "moderator": {
                    "full_name": f"{ctx.author}",
                    "id": ctx.author.id
                },
                "reason": reason
            })
            embed = discord.Embed(title = "Succesfully warned", description = f"{member} was successfully warned! | Reason: {reason}", color=discord.Color.embed_background())
            file = discord.File("assets/images/error.png")
            embed.set_thumbnail(url="attachment://error.png")
            await ctx.respond(file=file, embed=embed)
            if data[f"{member.guild.id}"][f"{member.id}"]["count"] == 3:
                await ctx.respond("Member has already have 3 warns")
                del data[f"{member.guild.id}"][f"{member.id}"]["warns"]
                if data[f"{ctx.guild.id}"] == {}:
                    del data[f"{ctx.guild.id}"]
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT `logs` FROM `sets` WHERE `id`={ctx.guild.id}")
                        result = cursor.fetchone()
                    connection.commit()
                except Exception as e:
                    print(f"Error: {e}")
                channel = self.bot.get_channel(result["logs"])
                member_data = member
                await ctx.guild.ban(member, reason=reason)
                await BanAndKicked().Chat(ctx, member_data, "Member has already have 3 warns").banned()
                if channel != None:
                    await BanAndKicked().Mod(ctx, channel, member_data, "Member has already have 3 warns").banned()
        with open("assets/data/warns.json", "w") as f:
            json.dump(data, f, indent=2)

    @mod.command(description="See member's warns")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def warns(self, ctx: discord.ApplicationContext, member: discord.Member):
        with open("assets/data/warns.json", "r") as f:
            data = json.load(f)
        embed = discord.Embed(description = f"{member.mention}'s warns", color=discord.Color.embed_background())
        embed.set_thumbnail(url = member.display_avatar)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
        if not str(member.id) in data[f"{member.guild.id}"]:
            embed.add_field(name="Warns", value=f"{member} doesn't have any warns!")
        else:
            for i in range(0, len(data[f"{member.guild.id}"][f"{member.id}"]["warns"])):
                embed.add_field(name = f"Warn #{i}", value = f"Reason `{data[f'{member.guild.id}'][f'{member.id}']['warns'][i]['reason']}`\nModerator: `{data[f'{member.guild.id}'][f'{member.id}']['warns'][i]['moderator']['full_name']}`, ID `{data[f'{member.guild.id}'][f'{member.id}']['warns'][i]['moderator']['id']}`")
        await ctx.respond(embed = embed)

    @mod.command(description="Removes all warns from member")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def removewarns(self, ctx: discord.ApplicationContext, member: discord.Member):
        with open("assets/data/warns.json", "r") as f:
            data = json.load(f)
        del data[f"{member.guild.id}"][f"{member.id}"]
        with open("assets/data/warns.json", "w") as f:
            json.dump(data, f, indent=2)
        embed = discord.Embed(title="Succesfully cleared warns", description=f"{member} was successfully cleared!", color=discord.Color.embed_background())
        file = discord.File("assets/images/success.png")
        embed.set_thumbnail(url="attachment://success.png")
        await ctx.respond(file=file, embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))