# MrRazamataz's RazBot
# Lucky command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class lucky(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="lucky")
    async def command_lucky(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            m = await ctx.channel.send(
                "OO yay a giveaway, my favourite thing to do. It's always fun to give back the epic community. Anyway, just react to the message with my reaction I have added and wait, it's as easy as that!")
            await m.add_reaction("👍")
            await asyncio.sleep(86400)
            await m.remove_reaction("👍", m.guild.me)
            m = await m.channel.fetch_message(m.id)
            member = random.choice(await m.reactions[0].users().flatten())
            await ctx.channel.send("The lucky winner is......")
            await asyncio.sleep(1)
            await ctx.channel.send("The")
            await asyncio.sleep(1)
            await ctx.channel.send("suspense")
            await asyncio.sleep(1)
            await ctx.channel.send("Here we go....")
            await asyncio.sleep(2)
            await ctx.channel.send(member.mention)
            await ctx.channel.send(
                "You have won! How very lucky of you! :). Now wait for <@611976655619227648> to notice and he will give you your prize!")
            print("Message sent in chat.")
        else:
            await ctx.channel.send("It seems you have no perms to run `raz!lucky`!")


def setup(client):
    client.add_cog(lucky(client))
