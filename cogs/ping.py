#MrRazamataz's RazBot
#Ping test command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def command_ping(self, ctx: commands.Context):
        await ctx.channel.send("Pong!")
        await ctx.message.add_reaction("👍")
        await asyncio.sleep(5)
        await ctx.message.remove_reaction("👍", ctx.guild.me)
        print("Message sent in chat.")


def setup(client):
    client.add_cog(ping(client))