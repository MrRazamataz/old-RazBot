# MrRazamataz's RazBot
# bugreport command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class bugreport(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="bugreport")
    async def command_cog(self, ctx, *, text):
        async with aiofiles.open("bug_data.txt", mode="a") as file:
            await file.write(f"{text}\n")
            await file.close()
            await ctx.send("Bug report has been saved.")


    @commands.command(name="bugreport.list")
    async def dm_all(self, ctx):
        await ctx.send("Reading bug reports from file:")
        async with aiofiles.open("bug_data.txt", mode="a") as bugreportlist:
            count = 0
            # Strips the newline character
            for line in bugreportlist:
                count += 1
                #print("Line{}: {}".format(count, line.strip()))
                await ctx.send(f"Line {count}: {line.strip}")


def setup(client):
    client.add_cog(bugreport(client))
