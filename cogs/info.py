# MrRazamataz's RazBot
# Info command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="info")
    async def command_info(self, ctx: commands.Context):
        await ctx.channel.send("Hi! I am RazBot, a Discord bot written in python by MrRazamataz! I am meant for helping out around the KC Discord sevrer whilst also having fun with the great community! You can download my source code/view more info at https://mrrazamataz.ga/archive/razbot . You can even add me to your server there!")


def setup(client):
    client.add_cog(info(client))
