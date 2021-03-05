# MrRazamataz's RazBot
# Unmute command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="unmute")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "Muted":
                await member.remove_roles(role)
                await ctx.channel.send("User has been unmuted.")

def setup(client):
    client.add_cog(unmute(client))
