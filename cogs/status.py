# MrRazamataz's RazBot
# status test command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles

quotation_mark = '"'


class status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="set_status.watch")
    async def set_status(self, ctx, status_text):
        if ctx.author.id == 611976655619227648:
            message = ctx.message
            status_output = quotation_mark + status_text + quotation_mark
            await ctx.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_text))
            await ctx.send(f"Status set to: `{status_output}`")
            print(f"Status Changed to {status_output}.")
        else:
            await ctx.send("This command can only be ran by MrRazamataz!")


def setup(client):
    client.add_cog(status(client))
