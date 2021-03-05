# MrRazamataz's RazBot
# slowmode command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class slowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="slowmode")
    async def setdelay(self, ctx, seconds: int):
        if ctx.author.guild_permissions.mute_members:
            if seconds > 21600:
                await ctx.channel.send("Sorry, it has to be less than 21600 seconds!")
            else:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
                print("Slowmode setting changed.")
        else:
            await ctx.channel.send("It seems you have no perms to run `raz!slowmode`!")

def setup(client):
    client.add_cog(slowmode(client))
