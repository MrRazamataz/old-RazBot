import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash_lockdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="lockdown", description="Lockdown the channel from non admins.")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(ctx.channel.mention + " is now in lockdown.")

def setup(client):
    client.add_cog(slash_lockdown(client))