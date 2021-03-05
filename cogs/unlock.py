# MrRazamataz's RazBot
# Unlock command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class unlock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(ctx.channel.mention + " has been unlocked.")


def setup(client):
    client.add_cog(unlock(client))
