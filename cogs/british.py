# MrRazamataz's RazBot
# meme command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import aiohttp

class british(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="british")
    async def british(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://old.reddit.com/r/uwotm8/random/.json') as r:
                    res = await r.json()

                    image= res[0]['data']['children'][0]['data']['url']
                    permalink= res[0]['data']['children'][0]['data']['permalink']
                    url = f'https://reddit.com{permalink}'
                    title = res[0]['data']['children'][0]['data']['title']
                    ups = res[0]['data']['children'][0]['data']['ups']
                    downs = res[0]['data']['children'][0]['data']['downs']
                    comments = res[0]['data']['children'][0]['data']['num_comments']

                    embed = discord.Embed(colour=discord.Color.blurple(), title=title, url=url)
                    embed.set_image(url=image)
                    embed.set_footer(text=f"🔺 {ups} | 🔻 {downs} | 💬 {comments}")
                    await ctx.send(embed=embed, content=None)


def setup(client):
    client.add_cog(british(client))
