# MrRazamataz's RazBot
# tools cog
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import youtube_dl
import aiohttp
import requests
import io
class tools(commands.Cog):
    def __init__(self, client):
        self.client = client

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
            ydl.download([video_info['webpage_url']])

        await ctx.send(f"<@{ctx.author.id}>, uploading `{deletefilename}`...")
        with open(f'{deletefilename}', 'rb') as fp:
            await ctx.send(file=discord.File(fp, f'{deletefilename}'))
        os.remove(f"{deletefilename}")

    @yt2mp3.error
    async def yt2mp3_error(self, ctx, error):
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
    async def triggered(self, ctx, member: discord.Member = None):
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



    @commands.command(name="currentvcs")
    async def currentvcs(self, ctx):
        vc_list = []
        for vc in self.client.voice_clients:
            for member in vc.members:
                vc_list.append(member)
        await ctx.send(f"There are {len(vc_list)} connected voice channels!")

def setup(client):
    client.add_cog(tools(client))
