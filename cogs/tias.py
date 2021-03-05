# MrRazamataz's RazBot
# tias command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class tias(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="tias")
    async def command_tias(self, ctx: commands.Context):
        await ctx.channel.send("https://tryitands.ee/")

def setup(client):
    client.add_cog(tias(client))
