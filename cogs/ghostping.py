# MrRazamataz's RazBot
# ghostping command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class ghostping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ghostping")
    async def ghostping(self, ctx, *, text):
        if ctx.author.guild_permissions.administrator:
            message = ctx.message
            await message.delete()


def setup(client):
    client.add_cog(ghostping(client))
