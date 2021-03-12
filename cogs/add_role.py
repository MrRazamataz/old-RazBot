# MrRazamataz's RazBot
# cog test command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class add_role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def add_role(self,ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(f"{ctx.author.name}, gave {user.name} the role: {role.name}.")

def setup(client):
    client.add_cog(add_role(client))
