import discord
from discord.ext import commands
import chat_exporter
import io
import pymysql
import pymysql.cursors

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    ticket = discord.SlashCommandGroup("ticket", "Anything related to tickets")

    @ticket.command(description="Close ticket")
    async def close(self, ctx: discord.ApplicationContext):
        if ctx.channel.name == f"{ctx.author.name}{ctx.author.discriminator}-ticket":
            class View(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
                async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
                    if interaction.user != ctx.author:
                        await interaction.response.send_message("You can't do that!", ephemeral=True)
                    else:
                        await interaction.message.delete()
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                            interaction.user: discord.PermissionOverwrite(view_channel = False),
                        }
                        await ctx.channel.edit(overwrites = overwrites)
                        embed = discord.Embed(description=f"Ticket closed by {interaction.user.mention}", color=discord.Color.embed_background())
                        msg: discord.Message = await ctx.channel.send(embed = embed)
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT `tickets_closed_category`, `tickets_opened_category` FROM `sets` WHERE `id`={ctx.guild.id}")
                                result = cursor.fetchone()
                            connection.commit()
                        except Exception as e:
                            print(f"Error: {e}")
                        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=result["tickets_closed_category"])
                        await ctx.channel.edit(category=category)
                        embed = discord.Embed(description="```\nTicket support control\n```")
                        transcript = discord.ui.Button(style=discord.ButtonStyle.grey, label="Transcript", emoji="📄")
                        reopen = discord.ui.Button(style=discord.ButtonStyle.gray, label="Reopen", emoji="🔓")
                        delete = discord.ui.Button(style=discord.ButtonStyle.danger, label="Delete", emoji="⛔")
                        async def ticket_transcript(interaction: discord.Interaction):
                            transcript = await chat_exporter.export(ctx.channel, limit=None, tz_info="UTC")
                            transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html",)
                            await interaction.response.send_message(file=transcript_file)
                        async def ticket_reopen(interaction: discord.Interaction):
                            overwrites = {
                                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                                ctx.author: discord.PermissionOverwrite(view_channel = True)
                            }
                            category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=result["tickets_opened_category"])
                            await ctx.channel.edit(category=category, overwrites = overwrites)
                            await msg.delete()
                            await msg1.delete()
                            embed = discord.Embed(description=f"Ticket opened by {interaction.user.mention}", color=discord.Color.embed_background())
                            await ctx.channel.send(embed = embed)
                        async def ticket_delete(interaction: discord.Interaction):
                            await interaction.channel.delete()
                        view = discord.ui.View(timeout=None)
                        transcript.callback = ticket_transcript
                        reopen.callback = ticket_reopen
                        delete.callback = ticket_delete
                        view.add_item(transcript)
                        view.add_item(reopen)
                        view.add_item(delete)
                        msg1: discord.Message = await ctx.channel.send(embed = embed, view = view)
                @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
                async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
                    if interaction.user != ctx.author:
                        await interaction.response.send_message("You can't do that!", ephemeral=True)
                    else:
                        await interaction.message.delete()
            await ctx.respond("Are you sure you would like to close this ticket?", view=View())
        else:
            await ctx.respond("You can't do that in this channel! Run this command in your ticket channel!", ephemeral=True)

    @ticket.command(description="Delete ticket")
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx: discord.ApplicationContext):
        if "ticket" in ctx.channel.name:
            class View(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red)
                async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
                    if ctx.author != interaction.user:
                        await interaction.response.send_message("You can't to that!", ephemeral=True)
                    else:
                        await interaction.channel.delete()
                @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
                async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
                    if ctx.author != interaction.user:
                        await interaction.response.send_message("You can't to that!", ephemeral=True)
                    else:
                        await interaction.message.delete()
            await ctx.respond("Are you sure you would like to delete this ticket?", view=View())
        else:
            await ctx.respond("You can't do that in this channel! Run this command in your ticket channel!", ephemeral=True)

    @ticket.command(description="Get channel's transcript")
    async def transcript(self, ctx: discord.ApplicationContext):
        transcript = await chat_exporter.export(ctx.channel, limit=None, tz_info="UTC")
        transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html",)
        await ctx.respond(file=transcript_file)

def setup(bot):
    bot.add_cog(Ticket(bot))