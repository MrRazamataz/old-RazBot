import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class slash_clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="clear", description="Clear the number of messages stated from the channel ran in.")
    async def clear(self, ctx, amount: int = None):
        if ctx.author.guild_permissions.administrator:
            if amount is None:
                await ctx.send("Please specify the amount of messages to delete in this command.")
            else:
                await ctx.channel.purge(limit=amount + 1)
                await ctx.send("Messages cleared.", hidden=True)
        else:
            await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")


def setup(client):
    client.add_cog(slash_clear(client))
