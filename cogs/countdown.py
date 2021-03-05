# MrRazamataz's RazBot
# Countdown command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class countdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="countdown")
    async def command_countdown(self, ctx: commands.Context):
        await ctx.message.add_reaction("🔟")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("🔟", ctx.guild.me)
        await ctx.message.add_reaction("9️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("9️⃣", ctx.guild.me)
        await ctx.message.add_reaction("8️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("8️⃣", ctx.guild.me)
        await ctx.message.add_reaction("7️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("7️⃣", ctx.guild.me)
        await ctx.message.add_reaction("6️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("6️⃣", ctx.guild.me)
        await ctx.message.add_reaction("5️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("5️⃣", ctx.guild.me)
        await ctx.message.add_reaction("4️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("4️⃣", ctx.guild.me)
        await ctx.message.add_reaction("3️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("3️⃣", ctx.guild.me)
        await ctx.message.add_reaction("2️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("2️⃣", ctx.guild.me)
        await ctx.message.add_reaction("1️⃣")
        await asyncio.sleep(1)
        await ctx.message.remove_reaction("1️⃣", ctx.guild.me)
        await ctx.message.add_reaction("👍")
        await asyncio.sleep(5)
        await ctx.message.remove_reaction("👍", ctx.guild.me)
        print("Countdown run.")


def setup(client):
    client.add_cog(countdown(client))
