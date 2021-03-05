# MrRazamataz's RazBot
# Ban command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} has been banned by {ctx.author.name}!")
        await ctx.message.add_reaction("👍")
        await asyncio.sleep(5)
        await ctx.message.remove_reaction("👍", ctx.guild.me)


def setup(client):
    client.add_cog(ban(client))
