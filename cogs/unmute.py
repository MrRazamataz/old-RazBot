# MrRazamataz's RazBot
# Unmute command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from discord_slash import cog_ext, SlashContext

class unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="unmute")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "Muted":
                await member.remove_roles(role)
                await ctx.channel.send("User has been unmuted.")
    @unmute.error
    async def unmute_error(self, ctx, error):
        await ctx.send("Sheeeeesh! \nThe correct formatting for this command is: \n`raz!unmute [user-ping]`")

    @cog_ext.cog_context_menu(target=ContextMenuType.USER, name="Unmute")
    @commands.has_permissions(ban_members=True)
    async def unmute_app(self, ctx: MenuContext):
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "Muted":
                await ctx.target_author.remove_roles(role)
                await ctx.send("User has been unmuted.", hidden=True)
def setup(client):
    client.add_cog(unmute(client))
