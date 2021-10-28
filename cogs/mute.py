# MrRazamataz's RazBot
# Mute command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from discord_slash import cog_ext, SlashContext

class mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="mute")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("This command failed due to role hierarchy! You are below the target user in this ~~pyramid scheme~~ discord server.")
            return
        else:
            guild = ctx.guild
            for role in guild.roles:
                if role.name == "Muted":
                    await member.add_roles(role)
                    await ctx.channel.send("User has been muted.")

    @mute.error
    async def mute_error(self, ctx, error):
        await ctx.send("Yo waddup, wait a moment matey! \nThe correct formatting for this command is: \n`raz!mute [user-ping]`")

    @cog_ext.cog_context_menu(target=ContextMenuType.USER, name="Mute")
    @commands.has_permissions(ban_members=True)
    async def mute_app(self, ctx: MenuContext):
        if ctx.target_author.top_role >= ctx.author.top_role:
            await ctx.send("This command failed due to role hierarchy! You are below the target user in this ~~pyramid scheme~~ discord server.")
            return
        else:
            guild = ctx.guild
            for role in guild.roles:
                if role.name == "Muted":
                    await ctx.target_author.add_roles(role)
                    await ctx.send("User has been muted.", hidden=True)
def setup(client):
    client.add_cog(mute(client))
