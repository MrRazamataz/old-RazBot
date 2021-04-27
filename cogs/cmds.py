# MrRazamataz's RazBot
# cmds command
import discord
from discord import reaction
from discord.ext import commands
from discord import reaction
import asyncio
import os
import aiofiles
# help pages
page1 = discord.Embed(title="RazBot Help Page 1", description="Use the buttons below to navigate between help pages. If there are no buttons, its because there was no input for 60 seconds, and was timed out. Run the `raz!cmds` command again to bning up another menu.", colour=discord.Colour.orange())
page2 = discord.Embed(title="RazBot Help Page 2", description="Commands:", colour=discord.Colour.orange())
page3 = discord.Embed(title="RazBot Help Page 3", description="Docs:", colour=discord.Colour.orange())
timeoutpage = discord.Embed(title="RazBot Help Page Timeout", description="This helppage has timed out after no input, please run `raz!cmds` again if you want to use it again", colour=discord.Colour.red())
class cmds(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.help_pages = [page1, page2, page3]
    @commands.command(name="cmds")
    async def cmds(self, ctx: commands.Context):
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]  # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=self.client.help_pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons,timeout=60.0)

            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return print("Cmds page timeout!")

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0

                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == u"\u27A1":
                    if current < len(self.client.help_pages) - 1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(self.client.help_pages) - 1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=self.client.help_pages[current])
def setup(client):
    client.add_cog(cmds(client))
