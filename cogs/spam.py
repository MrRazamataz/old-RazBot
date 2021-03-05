# MrRazamataz's RazBot
# Spam command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class spam(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="spam")
    async def command_spam(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.send("Spam is bad don't you know! A dm lesson is needed here.")
            await ctx.author.send("Spamming is very annoying and getting a bot to spam for you is not only scummy, but also against Discord TOS.")
            print("Message sent in chat.")
def setup(client):
    client.add_cog(spam(client))
