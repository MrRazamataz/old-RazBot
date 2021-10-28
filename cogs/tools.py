# MrRazamataz's RazBot
# tools cog
import discord
import random
from discord import reaction, Embed, Member
from discord.ext import commands, tasks
from random import choice
import asyncio
import os
import aiofiles
import youtube_dl
import aiohttp
import io
from pathlib import Path
import pysftp
import gc
from typing import Optional
from discord_slash import cog_ext, SlashContext
from datetime import datetime, timedelta
import json
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
ftp_server = "webserver ip"
ftp_username = "username"
ftp_password = "password"
vccountcheck = 0
class tools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.giveaways = []
    @cog_ext.cog_slash(name="yt2mp3", description="Convert ")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def yt2mp3_slash(self, ctx, link=None):
        if link is None:
            await ctx.send("Please provide the YouTube URL to process!")
            return
        await ctx.send("Processing... *may take some time depending on the size*")
        link = link.strip("<>")
        video_url = str(link)
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=video_url, download=False
        )
        filename = f"{video_info['title']}.{video_info['ext']}"
        deletefilename = f"{video_info['title']}.mp3"
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'keepvideo': False,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']]) #8283750
        if Path(f"{deletefilename}").stat().st_size > 8283750:
            await ctx.send(f"<@{ctx.author.id}>, file too big for discord, uploading to file server...")
            urlfilename = deletefilename.replace(" ", "-")
            os.rename(f"{deletefilename}", f"{urlfilename}")
            with pysftp.Connection(f'{ftp_server}', username=f"{ftp_username}", password=f"{ftp_password}", cnopts=cnopts) as sftp:
                with sftp.cd("public_html/yt2mp3/"):
                    sftp.put(f"{urlfilename}")
            filelink = f"https://razbot.xyz/yt2mp3/{urlfilename}"
            await ctx.send(f"<@{ctx.author.id}>, the file, `{deletefilename}`, has been uploaded; the link is: \n{filelink}")
            os.remove(f"{urlfilename}")


        else:
            await ctx.send(f"<@{ctx.author.id}>, uploading `{deletefilename}`...")
            with open(f'{deletefilename}', 'rb') as fp:
                await ctx.send(file=discord.File(fp, f'{deletefilename}'))
            os.remove(f"{deletefilename}")
    @commands.command(name="yt2mp3")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def yt2mp3(self, ctx, link=None):
        if link is None:
            await ctx.send("Please provide the YouTube URL to process!")
            return
        await ctx.send("Processing... *may take some time depending on the size*")
        link = link.strip("<>")
        video_url = str(link)
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=video_url, download=False
        )
        filename = f"{video_info['title']}.{video_info['ext']}"
        deletefilename = f"{video_info['title']}.mp3"
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'keepvideo': False,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']]) #8283750
        if Path(f"{deletefilename}").stat().st_size > 8283750:
            await ctx.send(f"<@{ctx.author.id}>, file too big for discord, uploading to file server...")
            urlfilename = deletefilename.replace(" ", "-")
            os.rename(f"{deletefilename}", f"{urlfilename}")
            with pysftp.Connection(f'{ftp_server}', username=f"{ftp_username}", password=f"{ftp_password}", cnopts=cnopts) as sftp:
                with sftp.cd("public_html/yt2mp3/"):
                    sftp.put(f"{urlfilename}")
            filelink = f"https://razbot.xyz/yt2mp3/{urlfilename}"
            await ctx.send(f"<@{ctx.author.id}>, the file, `{deletefilename}`, has been uploaded; the link is: \n{filelink}")
            os.remove(f"{urlfilename}")
            gc.collect()

        else:
            await ctx.send(f"<@{ctx.author.id}>, uploading `{deletefilename}`...")
            with open(f'{deletefilename}', 'rb') as fp:
                await ctx.send(file=discord.File(fp, f'{deletefilename}'))
            os.remove(f"{deletefilename}")
            gc.collect()
    @yt2mp3.error
    async def yt2mp3_error(self, ctx, error):
        await ctx.send(f"You are on a cooldown of that command for {error.retry_after:.2f}s!")
    @yt2mp3.error
    async def yt2mp3_slash_error(self, ctx, error):
        await ctx.send(f"You are on a cooldown of that command for {error.retry_after:.2f}s!")

    @commands.command(name="yt2mp4")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def yt2mp4(self, ctx, link=None):
        if vccountcheck == 0:
            if link is None:
                await ctx.send("Please provide the YouTube URL to process!")
                return
            await ctx.send("Processing... *may take some time depending on the size*")
            link = link.strip("<>")
            video_url = str(link)
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=video_url, download=False
            )
            filename = f"{video_info['title']}"
            options = {
                'format': 'best',  # choice of quality
                'extractaudio': False,  # only keep the audio
                'outtmpl': f"{filename}.%(ext)s",  # name the file the ID of the video
                'noplaylist': True,  # only download single song, not playlist
                'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4'
                    }],
                'listformats': False,  # print a list of the formats to stdout and exit

            }

            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([f"{video_url}"])
            urlfilename = filename.replace(" ", "-")
            os.rename(f"{filename}.mp4", f"{urlfilename}.mp4")
            await ctx.send(f"<@{ctx.author.id}>, uploading to file server...")
            with pysftp.Connection(f'{ftp_server}', username=f"{ftp_username}", password=f"{ftp_password}",
                                    cnopts=cnopts) as sftp:
                with sftp.cd("public_html/yt2mp4/"):
                    sftp.put(f"{urlfilename}.mp4")
            filelink = f"https://razbot.xyz/yt2mp4/{urlfilename}.mp4"
            await ctx.send(f"<@{ctx.author.id}>, the file, `{filename}.mp4`, has been uploaded; the link is: \n{filelink}")
            os.remove(f"{urlfilename}.mp4")
            gc.collect()
        else:
            await ctx.send("Sorry, but this command is disabled, because RazBot's network usage is higher then "
                           "average. \nPlease try again later.")
    @yt2mp4.error
    async def yt2mp4_error(self, ctx, error):
        await ctx.send(f"You are on a cooldown of that command for {error.retry_after:.2f}s!")
    @commands.command(name="triggered")
    async def triggered(self, ctx, member: discord.Member = None):
        if not member:  # if no member is mentioned
            member = ctx.author  # the user who ran the command will be the member
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:  # get users avatar as png with 1024 size
                imageData = io.BytesIO(await trigImg.read())  # read the image/bytes

                await trigSession.close()  # closing the session and;

                await ctx.reply(file=discord.File(imageData, 'triggered.gif'))  # sending the file
    @commands.command(name="gay")
    async def gay(self, ctx, member: discord.Member = None):
        if not member:  # if no member is mentioned
            member = ctx.author  # the user who ran the command will be the member
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:  # get users avatar as png with 1024 size
                imageData = io.BytesIO(await trigImg.read())  # read the image/bytes

                await trigSession.close()  # closing the session and;

                await ctx.reply(file=discord.File(imageData, 'gay.gif'))  # sending the file
    @commands.command(name="wasted")
    async def wasted(self, ctx, member: discord.Member = None):
        if not member:  # if no member is mentioned
            member = ctx.author  # the user who ran the command will be the member
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:  # get users avatar as png with 1024 size
                imageData = io.BytesIO(await trigImg.read())  # read the image/bytes

                await trigSession.close()  # closing the session and;

                await ctx.reply(file=discord.File(imageData, 'wasted.gif'))  # sending the file
    @commands.command(name="youtube")
    async def youtube(self, ctx, member: discord.Member=None, *, comment):
        try:
            if not member:  # if no member is mentioned
                member = ctx.author  # the user who ran the command will be the member
            await ctx.trigger_typing()
            async with aiohttp.ClientSession() as trigSession:
                async with trigSession.get(f'https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar_url_as(format="png", size=1024)}&username={member.name}&comment={comment}') as trigImg:  # get users avatar as png with 1024 size
                    imageData = io.BytesIO(await trigImg.read())  # read the image/bytes

                    await trigSession.close()  # closing the session and;

                    await ctx.reply(file=discord.File(imageData, 'ytcommennt.png'))  # sending the file
        except Exception as e:
            print(e)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nickall(self, ctx, *, name):
        await ctx.send(f"Setting everyone's names to `{name}`")
        guild = ctx.guild
        for member in guild.members:
            try:
                await member.edit(nick=f"{name}")
                await ctx.send(f"Changed: `{member.name}`.")
                await asyncio.sleep(1)
            except Exception as e:
                print(e)
                await ctx.send(f"Failed on member `{member.name}`. Put RazBot above the user roles to fix.")
                await asyncio.sleep(1)
                pass
        await ctx.send("Done.")

    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    async def server_info(self, ctx):
        embed = Embed(title="Server information",
                      colour=ctx.guild.owner.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name="RazBot", icon_url="https://mrrazamataz.ga/archive/RazBot.png")

        statuses = [len(list(filter(lambda m: str(m.status) == f"online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == f"idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == f"dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == f"offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", ctx.guild.region, True),
                  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title="User information",
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=target.avatar_url)

        fields = [("Name", str(target), True),
                  ("ID", target.id, True),
                  ("Bot?", target.bot, True),
                  ("Top role", target.top_role.mention, True),
                  ("Status", str(target.status).title(), True),
                  ("Activity",
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}",
                   True),
                  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosted", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(name="gcreate", aliases=["gstart"])
    @commands.has_permissions(manage_guild=True)
    async def gcreate(self, ctx, emoji="👍", *, description: str): #mins: int
        try:
            await ctx.message.delete()
            with open(f"giveaways/{ctx.guild.id}.json", "r") as f:
                await ctx.send("A giveaway is already running in this server!")
                return
        except:
            pass
        try:
            with open(f"giveaways/{ctx.guild.id}.json", "a+") as f:
                global giveaways
                pass
            id = str(ctx.guild.id)
            #gstart_time = datetime.now()
            #gend_time = gstart_time + timedelta(minutes=mins)
            #print(f"Giveaway System: \nStart: {gstart_time}. End: {gend_time}.")
            embed = Embed(title="Giveaway",
                          description=description,
                          colour=ctx.author.colour,
                          timestamp=datetime.utcnow())
            embed.add_field(name=f"React with {emoji} to enter.", value=f"Held by `{ctx.author.name}`.", inline=False)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(emoji)
            # "end": f"{gend_time}",
            save = {
                "desc": f"{description}",
                "emoji": f"{emoji}",
                "msgID": msg.id
            }
            with open(f"giveaways/{ctx.guild.id}.json", "w") as f:
                json.dump(save, f, indent=4)

        except Exception as e:
            await ctx.channel.purge(limit=1)
            await ctx.send(f"Error: \n`{e}`")
            await ctx.send("Giveaway aborted.", delete_after=1)
            os.remove(f"giveaways/{ctx.guild.id}.json")
            await ctx.send("Wagwan. \nThe correct usage of this command is: \n`raz!gstart <emoji> <giveaway description>`")
            return
        await ctx.author.send("Your giveaway has been created. Currently, it won't be automatically ended, so you can end the giveaway with `raz!gend`.")
    #@gcreate.error
    #async def gcreate_error(self, ctx, error):
        #await ctx.send("Wagwan. \nThe correct usage of this command is: \n`raz!gstart <emoji> <giveaway description>`")
    @commands.command(name="gend")
    @commands.has_permissions(manage_guild=True)
    async def gend(self, ctx):
        try:
            await ctx.message.delete()
            with open(f"giveaways/{ctx.guild.id}.json", "r") as f:
                #msg = await ctx.send(f"Using this command will override the automatic announcing of this giveaway, are you sure you wish to continue?")
                msg = await ctx.send("This will end the giveaway, are you sure you wish to continue?")
                await msg.add_reaction(u"\u2705")
                await msg.add_reaction(u"\U0001F6AB")

                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction,
                                                                                             user: user == ctx.author and reaction.emoji in [
                        u"\u2705", u"\U0001F6AB"], timeout=60.0)


                except asyncio.TimeoutError:
                    return

                else:
                    if reaction.emoji == u"\u2705":
                        await msg.delete()

                    else:
                        e = await ctx.channel.send("Operation aborted.")
                        await msg.delete()
                        await asyncio.sleep(2)
                        await e.delete()
                        return
        except:
            await ctx.send("No giveaway is running in this server!")
            return
        with open(f"giveaways/{ctx.guild.id}.json") as f:
            giveaway = json.load(f)
        m = await ctx.channel.fetch_message(giveaway["msgID"])
        await m.remove_reaction(giveaway["emoji"], m.guild.me)
        member = random.choice(await m.reactions[0].users().flatten())
        embed = Embed(title="Giveaway Ended",
                      description=giveaway["desc"],
                      colour=ctx.author.colour,
                      timestamp=datetime.utcnow())
        embed.add_field(name=f"`{member.name}` has won this giveaway.", value=f"Giveaway has ended.", inline=False)
        await m.edit(embed=embed)
        msg = await ctx.send(f"{member.mention} won the giveaway!")
        await msg.add_reaction("🔄")

        try:
            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction,
                                                                                     user: user == ctx.author and reaction.emoji in ["🔄"], timeout=60.0)


        except asyncio.TimeoutError:
            await msg.clear_reactions()
            os.rename(f"giveaways/{ctx.guild.id}.json", f"giveaways/OLD-{ctx.guild.id}.json")
            return

        else:
            if reaction.emoji == "🔄":
                member = random.choice(await m.reactions[0].users().flatten())
                await msg.edit(content=f"{member.mention} won the giveaway!")
                embed = Embed(title="Giveaway Ended",
                              description=giveaway["desc"],
                              colour=ctx.author.colour,
                              timestamp=datetime.utcnow())
                embed.add_field(name=f"`{member.name}` has won this giveaway.", value=f"Giveaway has ended.",
                                inline=False)
                await m.edit(embed=embed)
                await msg.clear_reactions()

        os.rename(f"giveaways/{ctx.guild.id}.json", f"giveaways/OLD-{ctx.guild.id}.json")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading giveaways...")
        print("Starting giveaway tasks loop...")
        #self.checkgiveaway.start()

    #@tasks.loop(minutes=1)
    #async def checkgiveaway(self):

def setup(client):
    client.add_cog(tools(client))
