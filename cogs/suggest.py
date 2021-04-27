# MrRazamataz's RazBot
# suggest command
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

    @commands.command(name="suggest")
    async def command_cog(self, ctx: commands.Context):
        print("Suggest ran")

def setup(client):
    client.add_cog(mod(client))
