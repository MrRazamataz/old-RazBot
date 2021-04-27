import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash_COMMAND(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="add_role", description="Add a role to a user.")
    async def add_role(self,ctx, user: discord.Member, role: discord.Role):
        if ctx.author.guild_permissions.administrator:
            await user.add_roles(role)
            await ctx.send(f"{ctx.author.name}, gave {user.name} the role: {role.name}.")
        else:
            await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")
def setup(client):
    client.add_cog(slash_COMMAND(client))