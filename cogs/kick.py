# MrRazamataz's RazBot
# cog test command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, arg1):
        await member.send(f"You have been kicked from `{member.guild.name}`. Kick reason: `{arg1}`")
        await member.kick(reason=arg1)
        await ctx.message.add_reaction("👍")
        await ctx.send(f"{member.name} has been kicked by {ctx.author.name}!")
        await ctx.message.remove_reaction("👍", ctx.guild.me)

def setup(client):
    client.add_cog(kick(client))

