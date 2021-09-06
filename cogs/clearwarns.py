# MrRazamataz's RazBot
# RazBot AutoMod
import discord
from discord.ext import commands
import asyncio
import aiofiles
import os
class clearwarns(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="clearwarns")
    @commands.has_permissions(kick_members=True)
    async def clearwarns(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Valid options: \n`server`, clear all warns for this server. \n`member`, clear all warns for the specific member.")

    @clearwarns.command()
    @commands.has_permissions(administrator=True)
    async def server(self, ctx):
        try:
            os.rename(f"{ctx.guild.id}.txt", f"backup-{ctx.guild.id}.txt")
            async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as warnfile:
                await warnfile.truncate(0)
                await warnfile.close()
            await ctx.send(f"This server's warns have been reset and can be restored with: \n`raz!clearwarns restore {ctx.guild.id}`")
        except Exception as e:
            await ctx.send(f"{e}")
            print(e)
    @clearwarns.command()
    @commands.has_permissions(ban_members=True)
    async def off(self, ctx):
        if self.check_if_string_in_file('automod.txt', f"{ctx.guild.id}\n"):
            with open("automod.txt", "r") as f:
                lines = f.readlines()
            with open("automod.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != f"{ctx.guild.id}":
                        f.write(line)
            await ctx.send("AutoMod has been disabled on this server!")
            with open("automod.txt", "r") as file:
                global discordserverids
                discordserverids = file.read().splitlines()
                print(discordserverids)
        else:
            await ctx.send("AutoMod isn't enabled on this server, you can enable it with: \n`raz!automod on`")
    @clearwarns.command()
    async def bannedwords(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Example usage: \n`raz!automod bannedwords [add/remove]`")

    def check_if_string_in_file(self, file_name, string_to_search):  # string checker
        """ Check if any line in the file contains given string """
        # Open the file in read only mode
        with open(file_name, 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if string_to_search in line:
                    return True
        return False



def setup(client):
    client.add_cog(clearwarns(client))
