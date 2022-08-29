import discord
from discord.ext import commands
import io
import chat_exporter
import contextlib
import ast
import pymysql
import pymysql.cursors

class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(style=discord.ButtonStyle.success, label="Create ticket", emoji="📩", custom_id="persistent_view:ticket")
        async def ticket(interaction: discord.Interaction):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT `tickets_opened_category`, `tickets_opened_category`, `tickets_admin` FROM `sets` WHERE `id`={interaction.guild.id}")
                    result = cursor.fetchone()
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
            member = interaction.user
            category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=result["tickets_opened_category"])
            admin: discord.Role = discord.utils.get(interaction.guild.roles, id=result["tickets_admin"])
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True),
                admin: discord.PermissionOverwrite(view_channel = True)
            }
            channel: discord.TextChannel = discord.utils.get(interaction.guild.text_channels, name=f"{interaction.user.name}{interaction.user.discriminator}-ticket")
            if channel == None:
                channel: discord.TextChannel = await interaction.guild.create_text_channel(f"{interaction.user} ticket", overwrites = overwrites, category=category)
                await interaction.response.send_message(f"Ticket created {channel.mention}", ephemeral=True)
                close = discord.ui.Button(style=discord.ButtonStyle.danger, label="Close", emoji="🔒", custom_id="persistent_view:close")
                async def ticket_close(interaction: discord.Interaction):
                    member2: discord.User = interaction.user
                    confirm = discord.ui.Button(style=discord.ButtonStyle.danger, label="Close", custom_id="persistent_view:confirm")
                    cancel = discord.ui.Button(style=discord.ButtonStyle.gray, label="Cancel", custom_id="persistent_view:cancel")
                    async def ticket_confirm(interaction: discord.Interaction):
                        if interaction.user != member2:
                            await interaction.response.send_message("You can't do that!", ephemeral=True)
                        else:
                            overwrites = {
                                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                                interaction.user: discord.PermissionOverwrite(view_channel = False),
                            }
                            await channel.edit(overwrites = overwrites)
                            embed = discord.Embed(description=f"Ticket closed by {interaction.user.mention}", color=discord.Color.embed_background())
                            msg: discord.Message = await channel.send(embed = embed)
                            category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=result["tickets_closed_category"])
                            await channel.edit(category=category)
                            await interaction.message.delete()
                            embed = discord.Embed(description="```\nTicket support control\n```")
                            transcript = discord.ui.Button(style=discord.ButtonStyle.grey, label="Transcript", emoji="📄", custom_id="persistent_view:transcript")
                            reopen = discord.ui.Button(style=discord.ButtonStyle.gray, label="Reopen", emoji="🔓", custom_id="persistent_view:reopen")
                            delete = discord.ui.Button(style=discord.ButtonStyle.danger, label="Delete", emoji="⛔", custom_id="persistent_view:delete")
                            async def ticket_transcript(interaction: discord.Interaction):
                                transcript = await chat_exporter.export(channel, limit=None, tz_info="UTC")
                                transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html",)
                                await interaction.channel.send(file=transcript_file)
                            async def ticket_reopen(interaction: discord.Interaction):
                                overwrites = {
                                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                                    member: discord.PermissionOverwrite(view_channel = True)
                                }
                                category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=result["tickets_opened_category"])
                                await channel.edit(category=category, overwrites = overwrites)
                                await msg.delete()
                                await msg1.delete()
                                embed = discord.Embed(description=f"Ticket opened by {interaction.user.mention}", color=discord.Color.embed_background())
                                await channel.send(embed = embed)
                            async def ticket_delete(interaction: discord.Interaction):
                                await interaction.channel.delete()
                            view = discord.ui.View(timeout=None)
                            transcript.callback = ticket_transcript
                            reopen.callback = ticket_reopen
                            delete.callback = ticket_delete
                            view.add_item(transcript)
                            view.add_item(reopen)
                            view.add_item(delete)
                            msg1: discord.Message = await channel.send(embed = embed, view = view)
                    async def ticket_cancel(interaction: discord.Interaction):
                        if interaction.user != member2:
                            await interaction.response.send_message("You can't do that!", ephemeral=True)
                        else:
                            await interaction.message.delete()
                    view = discord.ui.View(timeout=None)
                    confirm.callback = ticket_confirm
                    cancel.callback = ticket_cancel
                    view.add_item(confirm)
                    view.add_item(cancel)
                    await interaction.response.send_message("Are you sure you would like to close this ticket?", view = view)
                embed = discord.Embed(description="Support will be with you shortly\nTo close this ticket react with 🔒", color=discord.Color.embed_background())
                view = discord.ui.View(timeout=None)
                close.callback = ticket_close
                view.add_item(close)
                await channel.send(interaction.user.mention, embed = embed, view = view)
            else:
                await interaction.response.send_message(f"You already have ticket at {channel.mention}", ephemeral=True)
        button.callback = ticket
        self.add_item(button)

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bot.persistent_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.persistent_views_added == False:
            self.bot.add_view(Ticket())
            self.bot.persistent_views_added = True

    @commands.command()
    @commands.is_owner()
    async def file(self, ctx, path):
        try:
            await ctx.send(file=discord.File(path))
        except:
            await ctx.send("Wrong path")

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx: discord.ApplicationContext, *, cmd):
        fn_name = "_eval_expr"
        cmd = cmd[6:][:-4]
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)
        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    @commands.command()
    @commands.is_owner()
    async def eval2(self, ctx: discord.ApplicationContext, *, code):
        str_obj = io.StringIO()
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code[6:][:-4])
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
        await ctx.send(f'```{str_obj.getvalue()}```')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def say(self, ctx, *, content):
        await ctx.send(content)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Ticket", description="To create a ticket react with 📩", color=discord.Color.embed_background())
        await ctx.send(embed=embed, view=Ticket())

def setup(bot):
    bot.add_cog(Commands(bot))