# MrRazamataz's RazBot
# Mute command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="mute")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member):
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)
                await ctx.channel.send("User has been muted.")

def setup(client):
    client.add_cog(mute(client))
