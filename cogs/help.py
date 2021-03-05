#MrRazamataz's RazBot
#Help test command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def command_help(self, ctx: commands.Context):
        await ctx.channel.send("This is a bot made by MrRazamataz. For help with the minecraft server look at <#698580298182688809> or do /help on the Minecraft Server.")


def setup(client):
    client.add_cog(help(client))