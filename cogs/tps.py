# MrRazamataz's RazBot
# TPS command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class tps(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="tps")
    async def command_tps(self, ctx: commands.Context):
        await ctx.channel.send("/tps")
        print("TPS Done.")


def setup(client):
    client.add_cog(tps(client))
