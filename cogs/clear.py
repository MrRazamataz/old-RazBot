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
    async def clear(self, ctx, amount: int = None):
        if ctx.author.guild_permissions.administrator:
            if amount is None:
                await ctx.send("Please specify the amount of messages to delete in this command.")
            else:
                await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")


def setup(client):
    client.add_cog(clear(client))
