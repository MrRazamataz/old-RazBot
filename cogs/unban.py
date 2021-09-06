# MrRazamataz's RazBot
# Unban command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                await ctx.message.add_reaction("👍")
                await asyncio.sleep(5)
                await ctx.message.remove_reaction("👍", ctx.guild.me)
                return
    @unban.error
    async def unban_error(self, ctx, error):
        await ctx.send("Yeet! \nThe correct formatting for this command is: \n`raz!unban [user]`")
def setup(client):
    client.add_cog(mod(client))
