# MrRazamataz's RazBot
# kc.welcome command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class kcwelcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="kc.welcome")
    async def command_kcwelcome(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.channel.send(
            "Hello there KC Bot! Im sure we can get along even though we understand different languages. Good luck in this community!")


def setup(client):
    client.add_cog(kcwelcome(client))
