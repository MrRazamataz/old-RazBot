# MrRazamataz's RazBot
# Lockdown command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class lockdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="lockdown")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(ctx.channel.mention + " is now in lockdown.")

def setup(client):
    client.add_cog(lockdown(client))
