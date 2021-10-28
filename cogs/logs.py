# MrRazamataz's RazBot
# Logs Cog
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import datetime
from discord.utils import get
class mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        with open("logsettings.txt", "r") as file:
            global log_disabled
            log_disabled = file.read().splitlines()
            print(log_disabled)
        print(f"Log settings loaded.")
    @commands.group(name="log")
    @commands.has_permissions(administrator=True)
    async def log(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "To use RazBot logs, you need to create a channel called `#razbot-logs`. \nTo disable logs in a channel, "
                "you can use the command \n`raz!log off #channel-mention`")
    @log.command(name="off")
    @commands.has_permissions(administrator=True)
    async def logoff(self, ctx, channel: discord.TextChannel):
        global log_disabled
        print(log_disabled)
        if str(channel.id) in log_disabled:
            await ctx.channel.send("This channel already has logs disabled!")
        else:
            async with aiofiles.open("logsettings.txt", mode="a") as file:
                await file.write(f"{channel.id}"+ "\n")
                await file.close()
                await ctx.channel.send(f"{channel.mention} will no longer show in RazBot Logs.")
                with open("logsettings.txt", "r") as file:
                    log_disabled = file.read().splitlines()
                    print(log_disabled)
                print(f"Log settings updated.")

    @log.command(name="on")
    @commands.has_permissions(administrator=True)
    async def logon(self, ctx, channel: discord.TextChannel):
        global log_disabled
        if str(channel.id) in log_disabled:
            with open("logsettings.txt", "r") as f:
                lines = f.readlines()
            with open("logsettings.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != f"{channel.id}":
                        f.write(line)
            with open("logsettings.txt", "r") as file:
                log_disabled = file.read().splitlines()
                print(log_disabled)
            await ctx.send("Logs have been enabled again in this channel.")
        else:
            await ctx.send("Logs are enabled in this channel already! \nDisable them with: \n`raz!log off #channel-mention`")
            with open("logsettings.txt", "r") as file:
                log_disabled = file.read().splitlines()
                print(log_disabled)
            print(f"Log settings updated.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global log_disabled
        guild = message.guild
        log_channel = discord.utils.get(guild.channels, name="razbot-logs")
        if log_channel is None:
            return
        if not message.author.bot:
            if str(message.channel.id) in log_disabled:
                return
            else:
                embed = discord.Embed(title="{} deleted a message.".format(message.author.name),
                                      description="in {}:\n{}".format(message.channel.mention, message.content),
                                      color=0xFF0000, timestamp=datetime.datetime.utcnow(), )
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.set_footer(text=message.author.id)

                embed.add_field(name="Action:", value="Message has been deleted by user.",
                                inline=True)
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self,message_before, message_after):
        global log_disabled
        if str(message_after.channel.id) in log_disabled:
            return
        else:
            editEm = discord.Embed(title="Message edited".format(str(message_before.author)),
                                   description="", color=discord.Color.purple())
            editEm.add_field(name="**Before:**", value=message_before.content, inline=False)
            editEm.add_field(name="**After:**", value=message_after.content, inline=False)
            editEm.set_author(name=message_before.author, icon_url=message_before.author.avatar_url)
            editEm.timestamp = datetime.datetime.utcnow()
            log_channel = discord.utils.get(message_after.guild.channels, name="razbot-logs")
            if log_channel is None:
                return
            else:
                await log_channel.send(embed=editEm)
    @commands.Cog.listener()
    async def on_message(self, message):
        global log_disabled
        loadvar = ["raz!reloadvarforlogs"]
        if message.guild is None:
            return
        if get(message.guild.roles, name="RazBot-Spam-Mute"):
            role = get(message.guild.roles, name="RazBot-Spam-Mute")
            counter = 0
            with open("spam_detect.txt", "r+") as file:
                for lines in file:
                    if lines.strip("\n") == str(message.author.id):
                        counter += 1
                file.writelines(f"{str(message.author.id)}\n")
                if counter > 5:
                    await message.author.add_roles(role)
                    embed = discord.Embed(title=f"You have been automatically temp-muted in `{message.guild.name}`",
                                          description="",
                                          colour=discord.Colour.red())
                    embed.description += f"This was for spamming, and I, RazBot, picked up on it and muted you (the server owner has my spam mute turned on), sorry about that, but don't spam! \n This has been recorded in the RazBot logs."
                    try:
                        await message.author.send(embed=embed)
                    except Exception as e:
                        print(e)
                        pass
                    guild = message.guild
                    log_channel = discord.utils.get(guild.channels, name="razbot-logs")
                    if log_channel is None:
                        return
                    else:
                        embed = discord.Embed(title="{} was auto temp-muted for spamming.".format(message.author.name),
                                              description="in {}:\n{}".format(message.channel.mention, message.content),
                                              color=0xff7700, timestamp=datetime.datetime.utcnow(), )
                        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                        embed.set_footer(text=message.author.id)

                        embed.add_field(name="Action:", value="User has been temp-muted for 10 seconds.",
                                        inline=True)
                        await log_channel.send(embed=embed)
                    await asyncio.sleep(10)
                    await message.author.remove_roles(role)
        for word in loadvar:
            if not message.author.bot:
                pass
            else:
                if word in message.content:
                    with open("logsettings.txt", "r") as file:
                        global log_disabled
                        log_disabled = file.read().splitlines()
                        print(log_disabled)
                    print(f"Log settings loaded.")
def setup(client):
    client.add_cog(mod(client))
