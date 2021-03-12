# MrRazamataz's RazBot
# Quotes command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class quotes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="quotes")
    async def command_cog(self, ctx: commands.Context):
        await ctx.channel.send("woh woh we wah")
        print("Message sent in chat.")


def setup(client):
    client.add_cog(quotes(client))
