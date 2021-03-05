# MrRazamataz's RazBot
# 5minchannel command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class fiveminchannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="5minchannel")
    async def command_tempchannel(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await ctx.guild.create_text_channel('5min')
            await ctx.channel.send("The channel (#5min) will be deleted in 5 mins.")
            await asyncio.sleep(5)
            await ctx.guild.remove_text_channel('5min')  # lol this doesnt work yet
        else:
            await ctx.channel.send("It seems you have no perms to run `raz!5minchannel`!")


def setup(client):
    client.add_cog(fiveminchannel(client))
