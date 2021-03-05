# MrRazamataz's RazBot
# Plugins command

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


class plugins(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="plugins")
    async def command_info(self, ctx: commands.Context):
        async with ctx.channel.typing():
            await asyncio.sleep(2)
            await ctx.channel.send("Yoo lemme get that help coming youuuuuur waaayyy!")
            async with ctx.channel.typing():
                await asyncio.sleep(2)
                embed = discord.Embed(title='KC Plugin Help page:',description="This is still a work in progress but here is what is planned to be used to get help with plugin commands on KC instead of just linking to a badly made html site. However, until that day comes here is the page for your plugin help.\n http://kingdomscrusade.net/plugins.html",olor=0x00ff00)
                embed.set_image(url='https://mrrazamataz.ga/archive/RazBot.png')
                embed.set_footer(text='RazBot', icon_url='https://mrrazamataz.ga/archive/RazBot.png')
                await ctx.send(embed=embed)
def setup(client):
    client.add_cog(plugins(client))
