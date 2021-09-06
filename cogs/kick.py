# MrRazamataz's RazBot
# kick cog command

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
        if member.top_role >= ctx.author.top_role:
            await ctx.send("This command failed due to role hierarchy! You are below the target user in this ~~pyramid scheme~~ discord server.")
            return
        else:
            await member.send(f"You have been kicked from `{member.guild.name}`. Kick reason: `{arg1}`")
            await member.kick(reason=arg1)
            await ctx.message.add_reaction("👍")
            await ctx.send(f"{member.name} has been kicked by {ctx.author.name}!")
            await ctx.message.remove_reaction("👍", ctx.guild.me)

    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send("Hold it, hold it! \nThe correct formatting for this command is: \n`raz!kick [user]`")
def setup(client):
    client.add_cog(kick(client))

