# MrRazamataz's RazBot
# wiki command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import wikipedia

class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['wikipedia','define'])
    async def wiki(self, ctx, *, query):
        em = discord.Embed(title=str(query))
        em.set_footer(text='Powered by wikipedia.org')
        try:
            result = wikipedia.summary(query)
            if len(result) > 2000:
                em.color = discord.Color.red()
                em.description = f"Result is too long. View the website [here](https://wikipedia.org/wiki/{query.replace(' ', '_')}), or just google the subject."
                return await ctx.send(embed=em)
            em.color = discord.Color.green()
            em.description = result
            await ctx.send(embed=em)
        except wikipedia.exceptions.DisambiguationError as e:
            em.color = discord.Color.red()
            options = '\n'.join(e.options)
            em.description = f"**Options:**\n\n{options}"
            await ctx.send(embed=em)
        except wikipedia.exceptions.PageError:
            em.color = discord.Color.red()
            em.description = 'Error: Page not found.'
            await ctx.send(embed=em)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author

        embed = discord.Embed(title=f"Avatar for {member.name}",description=f"**Link as**\n[png]({member.avatar_url_as(format='png', size=1024)}) | [jpg]({member.avatar_url_as(format='jpg', size=1024)}) | [webp]({member.avatar_url_as(format='webp', size=1024)})", colour=discord.Color.blurple())
        embed.set_image(url=str(member.avatar_url))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ban(client))
