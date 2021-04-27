import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash_kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="kick", description="Kick a user from the server.")
    async def kick(self,ctx, user: discord.Member, role: discord.Role, member: discord.Member):
        await member.kick()
        await ctx.message.add_reaction("👍")
        await ctx.send(f"{member.name} has been kicked by {ctx.author.name}!")
        await ctx.author.send(f"You kicked {member.display_name}.")
        await ctx.message.remove_reaction("👍", ctx.guild.me)
def setup(client):
    client.add_cog(slash_kick(client))