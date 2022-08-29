import discord

class BanAndKicked():
    """A class to represent other classes."""
    class Chat():
        """
        A class to represent a Chat.

        Attributes
        ----------
        ctx : `discord.ApplicationContext`
            A context for `author` and `respond`
        member : `discord.Member`
            A discord member to take name, id and avatar
        reason : Optional[`str`]
            Reason of ban/kick

        Methods
        -------
        kicked():
            Returning `ctx.respond` with kick embed
        banned():
            Returning `ctx.respond` with ban embed
        """
        def __init__(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None):
            self.ctx = ctx
            self.member = member
            self.reason = reason
            
        def kicked(self) -> discord.Embed:
            """
            Returning `ctx.respond` with kick embed
            """
            embed = discord.Embed(title="Successfully kicked!", description=f"{self.member} was successfully kicked!", color=discord.Color.embed_background())
            file = discord.File("assets/images/success.png")
            embed.set_thumbnail(url="attachment://success.png")
            embed.add_field(name="Reason", value=f"`{self.reason}`")
            embed.add_field(name="ID", value=f"`{self.member.id}`", inline=False)
            embed.set_footer(text=f"Requested by: {self.ctx.author}", icon_url=self.ctx.author.display_avatar)
            return self.ctx.respond(file=file, embed=embed)

        def banned(self) -> discord.Embed:
            """
            Returning `ctx.respond` with ban embed
            """
            embed = discord.Embed(title="Successfully banned!", description=f"{self.member} was successfully banned!", color=discord.Color.embed_background())
            file = discord.File("assets/images/success.png")
            embed.set_thumbnail(url="attachment://success.png")
            embed.add_field(name="ID", value=f"`{self.member}`", inline=False)
            embed.set_footer(text=f"Requested by: {self.ctx.author}", icon_url=self.ctx.author.display_avatar)
            return self.ctx.respond(file=file, embed=embed)

    class Mod():
        """
        A class to represent a Mod chat.

        Attributes
        ----------
        ctx : `discord.ApplicationContext`
            A context for `author` and `respond`
        channel : `discord.TextChannel`
            A channel to send embed in
        member : `discord.Member`
            A discord member to specify name, id, avatar and name 
        reason : Optional[`str`]
            Reason of ban/kick

        Methods
        -------
        kicked():
            Returning `channel.send` with kick embed
        banned():
            Returning `channel.send` with ban embed
        """
        def __init__(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, member: discord.Member, reason: str):
            self.ctx = ctx
            self.channel = channel
            self.member = member
            self.reason = reason
            
        def kicked(self) -> discord.Embed:
            """
            Returning `channel.send` with kick embed
            """
            embed = discord.Embed(title="User kicked", color=discord.Color.embed_background())
            embed.set_thumbnail(url=self.member.display_avatar)
            embed.add_field(name="User", value=f"{self.member} | ID: `{self.member.id}`")
            embed.add_field(name="Moderator", value=f"{self.ctx.author.mention}")
            embed.set_footer(text=f"Reason: {self.reason}")
            return self.channel.send(embed=embed)

        def banned(self) -> discord.Embed:
            """
            Returning `channel.send` with ban embed
            """
            embed = discord.Embed(title="User banned", color=discord.Color.embed_background())
            embed.set_thumbnail(url=self.member.display_avatar)
            embed.add_field(name="User", value=f"{self.member} | ID: `{self.member.id}`")
            embed.add_field(name="Moderator", value=f"{self.ctx.author.mention}")
            embed.set_footer(text=f"Reason: {self.reason}")
            return self.channel.send(embed=embed)