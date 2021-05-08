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
page1 = discord.Embed(title="RazBot Help Page 1", description="Use the buttons below to navigate between help pages. If there are no buttons, its because there was no input for 60 seconds, and was timed out. Run the `raz!help` command again to bring up another menu.", colour=discord.Colour.orange())
page2 = discord.Embed(title="RazBot Help Page 2", description="Commands:", colour=discord.Colour.orange())
page2.set_thumbnail(url="https://www.mrrazamataz.ga/archive/RazBot.png")
page2.add_field(name="Moderation:", value="\u200b", inline=False)
page2.add_field(name="Ban:", value="raz!ban [user-ping] [reason], bans the specifed user from the server.", inline=True)
page2.add_field(name="Unban: ", value="`raz!unban [user]`, unbans the specifed user from the server.", inline=True)
page2.add_field(name="Mute: ", value="`raz!mute [user-ping]`, adds the muted role to the user.", inline=True)
page2.add_field(name="Unmute: ", value="`raz!unmute [user-ping]`, removes the muted role fron the user.", inline=True)
page2.add_field(name="Temp Mute:", value="`raz!tempmute [user-ping] [Number] [s/m/h/d]`, tempmute the user for the amount of time specified. **Note: The space (` `) between `[Number]` and `[s/m/h/d]` is required.**", inline=True)
page2.add_field(name="Kick:", value="`raz!kick [user-ping]`, kicks the specifed user from the server.", inline=True)
page2.add_field(name="Clear:", value="`raz!clear [number]`, clears the specified amount of messages.", inline=True)
page2.add_field(name="Lockdown:", value="`raz!lockdown`, locks down the channel for non admins/staff.", inline=True)
page2.add_field(name="Unlock:", value="`raz!unlock`, unlockdowns the channel after a `raz!lockown`.", inline=True)
page2.add_field(name="Say:", value="`raz!say [message]`, make the bot repeat the messasge.", inline=True)
page2.add_field(name="Warn: ", value="`raz!warn [user-ping] [reason]`, add a warning to the user in that server.", inline=True)
page2.add_field(name="View Warnings:", value="`raz!warnings [user-ping]`. view the warnings of the user for that server.", inline=True)
page2.add_field(name="Slowmode:", value="`raz!slowmode <seconds>`, puts the channel in slowmode for the specified amount, set to 0 to disable slowmode.", inline=False)
page2.add_field(name="Useful Commands:", value="\u200b", inline=True)
page2.add_field(name="Add Reaction Role:", value="`raz!set_reaction [RoleName] [MessageID] [Emoji]`, adds a reaction which users can react to to give themselves the specifed role (works multiple times on the same message with differnet reactions).", inline=True)
page2.add_field(name="Add Role:", value="`raz!add_role @usermention [role name]`, gives the user the role specifed. ", inline=True)
page2.add_field(name="Suggest:", value="`raz!suggest <text>`, like vote, but for normal users (only adds reactions).", inline=True)
page2.add_field(name="Vote:", value="`raz!vote <text>`, adds vote reactions and explanation. ", inline=True)
page2.add_field(name="Version:", value="`raz!ver`, shows the version of the bot.", inline=True)
page2.add_field(name="Lucky (Giveaway):", value="`raz!lucky`, adds a reaction and after 24hours, picks a random person from the reactions.", inline=True)
page3 = discord.Embed(title="RazBot Help Page 3", description="Docs:", colour=discord.Colour.orange())
timeoutpage = discord.Embed(title="RazBot Help Page Timeout", description="This helppage has timed out after no input, please run `raz!cmds` again if you want to use it again", colour=discord.Colour.red())
class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.help_pages = [page1, page2, page3]
    @commands.command(name="help")
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
    client.add_cog(help(client))
