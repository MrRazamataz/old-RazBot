# MrRazamataz's RazBot
# Clear command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        if amount is None:
            await ctx.send("Please specify the amount of messages to delete in this command.")
        else:
                await ctx.channel.purge(limit=amount + 1)

    @clear.error
    async def clear_error(self, ctx, error):
        await ctx.send("Man this one simple... \nThe correct formatting for this command is: \n`raz!clear [number]`")
def setup(client):
    client.add_cog(clear(client))
