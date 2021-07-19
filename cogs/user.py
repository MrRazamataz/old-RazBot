# MrRazamataz's RazBot
# userinfo command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles


class user(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='user')
    #@commands.cooldown(1, 5, commands.BucketType.user)
    async def user(ctx, user: discord.Member = None):
        if not user:
            roles = [role for role in ctx.self.author.roles]
            user_embed = discord.Embed(color=ctx.self.author.color, timestamp=ctx.self.message.created_at)
            user_embed.set_author(name=f'User info: {ctx.self.author}')
            user_embed.set_thumbnail(url=ctx.self.author.avatar_url)
            user_embed.set_footer(text=f'Requested by {ctx.self.author}', icon_url=ctx.self.author.avatar_url)
            user_embed.add_field(name='ID:', value=ctx.self.author.id)
            user_embed.add_field(name='Display Name:', value=f'{ctx.self.author}')
            user_embed.add_field(name='Created at:',
                                 value=ctx.self.author.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            user_embed.add_field(name='Joined at:', value=ctx.self.author.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            user_embed.add_field(name=f'Roles: ({len(roles)})', value=' '.join([role.mention for role in roles]))
            user_embed.add_field(name='Bot?', value=ctx.self.author.bot)
            await ctx.self.send(embed=user_embed)
        else:
            roles = [role for role in user.roles]
            user_embed = discord.Embed(color=user.color, timestamp=ctx.self.message.created_at)
            user_embed.set_author(name=f'User info: {user}')
            user_embed.set_thumbnail(url=user.avatar_url)
            user_embed.set_footer(text=f'Requested by {ctx.self.author}', icon_url=ctx.self.author.avatar_url)
            user_embed.add_field(name='ID:', value=user.id)
            user_embed.add_field(name='Display Name:', value=f'{user}')
            user_embed.add_field(name='Created at:', value=user.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            user_embed.add_field(name='Joined at:', value=user.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            user_embed.add_field(name=f'Roles: ({len(roles)})', value=' '.join([role.mention for role in roles]))
            user_embed.add_field(name='Bot?', value=user.bot)
            await ctx.self.send(embed=user_embed)

def setup(client):
    client.add_cog(user(client))
