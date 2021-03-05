# MrRazamataz's RazBot
# permlist command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class permlist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="permlist")
    async def command_permlist(self, ctx: commands.Context):
        await ctx.author.send("https://www.mrrazamataz.ga/archive/discord%20perms.png")
        await ctx.author.send("Taken from: https://discordpy.readthedocs.io/en/latest/api.html?highlight=permissions#discord.Permissions")
        await ctx.channel.send("You got mail!")
        await ctx.message.add_reaction("👍")
        await asyncio.sleep(5)
        await ctx.message.remove_reaction("👍", ctx.guild.me)
        print("Permlist command ran")

def setup(client):
    client.add_cog(permlist(client))
