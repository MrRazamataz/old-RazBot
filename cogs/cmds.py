#MrRazamataz's RazBot
#Help test command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os

class cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="cmds")
    async def command_help(self, ctx: commands.Context):
        await ctx.channel.send("For commands, look on the second page of `raz!help`.")

def setup(client):
    client.add_cog(cmds(client))