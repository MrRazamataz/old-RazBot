# MrRazamataz's RazBot
# say command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="say")
    async def say(self, ctx, *, text):
        if ctx.author.guild_permissions.administrator:
            message = ctx.message
            await message.delete()
            await ctx.send(f"{text}")
        else:
            message = ctx.message
            await message.delete()
            await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")


def setup(client):
    client.add_cog(say(client))
