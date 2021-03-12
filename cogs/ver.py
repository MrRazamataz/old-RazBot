# MrRazamataz's RazBot
# cog test command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class ver(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ver")
    async def command_ver(self, ctx: commands.Context):
        async with ctx.channel.typing():
            await asyncio.sleep(2)
            await ctx.channel.send("This version of the bot is running version 3.6, with new add role command.")
            await ctx.message.add_reaction("3️⃣")
            await ctx.message.add_reaction("⚫")
            await ctx.message.add_reaction("6️⃣")
            print("Message sent in chat.")


def setup(client):
    client.add_cog(ver(client))
