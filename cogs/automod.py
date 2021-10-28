# MrRazamataz's RazBot
# RazBot AutoMod
import discord
from discord.ext import commands
import asyncio
import aiofiles
import datetime
from datetime import datetime
from discord_slash import cog_ext, SlashContext
from time import time, ctime
class automod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="automod")
    @commands.has_permissions(ban_members=True)
    async def automod(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("RazBot AutoMod aims to protect and keep your server clean with ease. \nTo enable it simply run the command: \n`raz!automod on`")

    @cog_ext.cog_subcommand(description="AutoMod Information", base_description="AutoMod settings and info", base="automod", name="info")
    async def automod_slash_info(self, ctx):
        await ctx.send("RazBot AutoMod aims to protect and keep your server clean with ease. \nTo enable it simply run the command: \n`/automod on`")

    @cog_ext.cog_subcommand(description="AutoMod on", base="automod", name="on")
    async def automod_slash_on(self, ctx):
        if self.check_if_string_in_file('automod.txt', f"{ctx.guild.id}\n"):
            await ctx.channel.send(
                "AutoMod is already enabled in this discord server! You can disable it with: \n`/automod off`")
        else:
            async with aiofiles.open("automod.txt", mode="a") as file:
                await file.write(f"{ctx.guild.id}\n")
                await file.close()
            await ctx.send("AutoMod has been enabled on this discord server!")
            with open("automod.txt", "r") as file:
                global discordserverids
                discordserverids = file.read().splitlines()
                print(discordserverids)
    @cog_ext.cog_subcommand(description="AutoMod off", base="automod", name="off")
    async def automod_slash_off(self, ctx):
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
            await ctx.send("AutoMod isn't enabled on this server, you can enable it with: \n`/automod on`")
    @automod.command()
    @commands.has_permissions(ban_members=True)
    async def on(self, ctx):
        if self.check_if_string_in_file('automod.txt', f"{ctx.guild.id}\n"):
            await ctx.channel.send("AutoMod is already enabled in this discord server! You can disable it with: \n`raz!automod off`")
        else:
            async with aiofiles.open("automod.txt", mode="a") as file:
                await file.write(f"{ctx.guild.id}\n")
                await file.close()
            await ctx.send("AutoMod has been enabled on this discord server!")
            with open("automod.txt", "r") as file:
                global discordserverids
                discordserverids = file.read().splitlines()
                print(discordserverids)
    @automod.command()
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
    @automod.group()
    async def bannedwords(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Example usage: \n`raz!automod bannedwords [add/remove]`")
    @bannedwords.command()
    async def list(self, ctx):
        await ctx.send("I will attempt to DM you the list of AutoMod banned words!")
        global banned_words
        try:
            await ctx.author.send(f"Banned words: \n`{banned_words}`")
            await ctx.send("You got mail!")
        except discord.Forbidden:
            await ctx.send("Failed to DM you, are your DMs open?")
    @bannedwords.command()
    async def add(self, ctx, message):
        if ctx.author.id == 611976655619227648:
            if self.check_if_string_in_file('bannedwords.txt', f"{message}\n"):
                await ctx.channel.send("That word is already in the AutoMod banned words list!")
                await message.delete()
            else:
                async with aiofiles.open("bannedwords.txt", mode="a") as file:
                    await file.write(f"{message}\n")
                    await file.close()
                await ctx.channel.send("That word has been added to the AutoMod banned word list!")
                with open("bannedwords.txt", "r") as file:
                    global banned_words
                    banned_words = file.read().splitlines()
                    print(banned_words)
                await message.delete()
        else:
            await ctx.send("This command can only be used by MrRazamataz.")
    @bannedwords.command()
    async def remove(self, ctx, message):
        if ctx.author.id == 611976655619227648:
            if self.check_if_string_in_file('bannedwords.txt', f"{message}\n"):
                with open("bannedwords.txt", "r") as f:
                    lines = f.readlines()
                with open("bannedwords.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != f"{message}":
                            f.write(line)
                await ctx.send("That word has been removed from the AutoMod banned words list!")
                with open("bannedwords.txt", "r") as file:
                    global banned_words
                    banned_words = file.read().splitlines()
                    print(banned_words)
            else:
                await ctx.send("That word wasn't found in the AutoMod banned words list file!")
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading AutoMod servers...")
        with open("automod.txt", "r") as file:
            global discordserverids
            discordserverids = file.read().splitlines()
            print(discordserverids)
        print("Loading banned words...")
        with open("bannedwords.txt", "r") as file:
            global banned_words
            banned_words = file.read().splitlines()
            print(banned_words)
        self.client.removing_channels = {}
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        guildid = str(message.guild.id)
        loadvar = ["raz!reloadvarforautomod"]
        for word in loadvar:
            if not message.author.bot:
                pass
            else:
                if word in message.content:
                    print("Loading AutoMod words...")
                    with open("automod.txt", "r") as file:
                        global discordserverids
                        discordserverids = file.read().splitlines()
                        print(discordserverids)
                    print("Loading banned words...")
                    with open("bannedwords.txt", "r") as file:
                        global banned_words
                        banned_words = file.read().splitlines()
                        print(banned_words)
        for word in banned_words:
            if not message.author.bot:
                if guildid in discordserverids:
                    if word in message.content.lower():
                        await message.delete()
                        await message.channel.send(f"Hey <@{message.author.id}>, please refrain from using banned/NSFW words.")
                        guild = message.guild
                        log_channel = discord.utils.get(guild.channels, name="razbot-logs")
                        if log_channel is None:
                            pass
                        else:
                            embed = discord.Embed(
                                title="{} posted a banned word.".format(message.author.name),
                                description="in {}:\n{}".format(message.channel.mention, message.content),
                                color=0xff7700, timestamp=datetime.datetime.utcnow(), )
                            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                            embed.set_footer(text=message.author.id)

                            embed.add_field(name="Action:", value="Message has been deleted.",
                                            inline=True)
                            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        guildid = str(message_after.guild.id)
        for word in banned_words:
            if not message_after.author.bot:
                if guildid in discordserverids:
                    if word in message_after.content.lower():
                        await message_after.delete()
                        await message_after.channel.send(f"Hey <@{message_after.author.id}>, please refrain from using banned/NSFW words. \nTrying to be smart by edting your messages doesn't bypass me, mate.")
                        guild = message_after.guild
                        log_channel = discord.utils.get(guild.channels, name="razbot-logs")
                        if log_channel is None:
                            pass
                        else:
                            embed = discord.Embed(
                                title="{} edited a message into a banned word.".format(message_after.author.name),
                                description="in {}:\n{}".format(message_after.channel.mention, message_after.content),
                                color=0xff7700, timestamp=datetime.datetime.utcnow(), )
                            embed.set_author(name=message_after.author, icon_url=message_after.author.avatar_url)
                            embed.set_footer(text=message_after.author.id)

                            embed.add_field(name="Action:", value="Message has been deleted.",
                                            inline=True)
                            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        async for event in guild.audit_logs(action=discord.AuditLogAction.channel_delete,
                                            limit=3):  # get last 3 incase someone delete at exact time?
            if event.user is not self.client.user:
                if event.target.id == channel.id:
                    try:
                        amount, last = self.client.removing_channels[event.user.id]
                        if time() - last < 5:  # 5 seconds between each creation will be flagged
                            amount += 1
                            last = time()

                            if amount >= 3:
                                await event.user.ban(reason="For deleting 3 or more channels at once.")
                                guild = event.guild
                                log_channel = discord.utils.get(guild.channels, name="razbot-logs")
                                if log_channel is None:
                                    return
                                else:
                                    await log_channel.send(f"Successfully banned {event.user.name} for deleting more than 3 channels at once.")
                                return

                        else:  # otherwise reset the time
                            amount = 1
                            last = 0

                        self.client.removing_channels[event.user.id] = (amount, last)

                    except KeyError:
                        self.client.removing_channels[event.user.id] = (1, time())

                    except Exception as error:
                        print(guild.id, f"failed at {error} whilst calculating channel deletion amounts.")

                    finally:
                        break
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
    client.add_cog(automod(client))
