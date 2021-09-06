# MrRazamataz's RazBot
# tempmute cog command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class tempmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="tempmute", pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def tempmute(self, ctx, member: discord.Member, time: int, d, *, reason=None):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("This command failed due to role hierarchy! You are below the target user in this ~~pyramid scheme~~ discord server.")
            return
        else:
            guild = ctx.guild
    
            for role in guild.roles:
                if role.name == "Muted":
                    await member.add_roles(role)

                    embed = discord.Embed(title="RazBot Mute System:", description=f"{member.mention} has been tempmuted ",
                                          colour=discord.Colour.dark_purple())
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.add_field(name="Mute duration:", value=f"{time}{d}", inline=False)
                    await ctx.send(embed=embed)

                    if d == "s":
                        await asyncio.sleep(time)

                    if d == "m":
                        await asyncio.sleep(time * 60)

                    if d == "h":
                        await asyncio.sleep(time * 60 * 60)

                    if d == "d":
                        await asyncio.sleep(time * 60 * 60 * 24)

                    await member.remove_roles(role)

                    embed = discord.Embed(title="RazBot Mute System: ",
                                          description=f"Unmuted (tempmute expired): -{member.mention} ",
                                          colour=discord.Colour.dark_purple())
                    await ctx.send(embed=embed)

                    return
def setup(client):
    client.add_cog(tempmute(client))
