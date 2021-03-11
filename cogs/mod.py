# MrRazamataz's RazBot
# cog test command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="mod")
    async def command_cog(self, ctx: commands.Context):
        await ctx.channel.send("It worked well done!")
        print("Message sent in chat.")


def setup(client):
    client.add_cog(mod(client))
