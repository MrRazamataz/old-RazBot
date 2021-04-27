# MrRazamataz's RazBot
# wait for command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class wait_for(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="wait_for")
    async def command_wait_for(self, ctx: commands.Context):
        msg = await ctx.channel.send("Do you play on KC?")
        await msg.add_reaction(u"\u2705")
        await ctx.message.add_reaction(u"\U0001F6AB")

        try:
            reaction, user = await commands.wait_for("reaction_add",check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=30.0)


        except asyncio.TimeoutError:
            await ctx.channel.send("Damn, you really not gonna respond like that, ok.")

        else:
            if reaction.emoji == u"\u2705":
                await ctx.channel.send("Thank you!")

            else:
                await ctx.channel.send("Why not")

def setup(client):
    client.add_cog(wait_for(client))
