# MrRazamataz's RazBot
# Warning command command
# CURRENTLY THE WARNING SYSTEM ISNT IN THIS COG, ITS IN THE MAIN FILE.
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class warn(commands.Cog):
    def __init__(self, client):
        self.client = client
    intents = discord.Intents.default()
    intents.members = True
    bot.warnings = {}  # guild_id : {member_id: [count, [(admin_id, reason)]]}

    @commands.command(name="warn")
    @commands.has_permissions(ban_members=True)
    async def command_warn(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            return await ctx.send("User not found... Did you enter one?")

        if reason is None:
            return await ctx.send("Oii mate you need to provide a warn reason!")
    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = bot.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{member.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

def setup(client):
    client.add_cog(warn(client))
