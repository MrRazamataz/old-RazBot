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
    async def ban(self, ctx, member: discord.Member, *, arg1, reason=None):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("This command failed due to role hierarchy! You are below the target user in this ~~pyramid scheme~~ discord server.")
            return
        else:
            await member.send(f"You have been banned from `{member.guild.name}`. Ban reason: `{arg1}`")
            await member.ban(reason=arg1)
            await ctx.send(f"{member.name} has been banned by `{ctx.author.name}`, with the reason `{arg1}`!")
            await ctx.message.add_reaction("👍")
            await asyncio.sleep(2)
            await ctx.message.remove_reaction("👍", ctx.guild.me)

    @ban.error
    async def ban_error(self, ctx, error):
        await ctx.send("Woah steady on! \nThe correct formatting for this command is: \n`raz!ban [@user-ping] [reason]`")

def setup(client):
    client.add_cog(ban(client))
