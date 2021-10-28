# MrRazamataz's RazBot
# stick bug
# credit for stick bug code would goes to https://github.com/n0spaces/get-stick-bugged-lol
from discord.ext import commands
import discord
import asyncio
import os
import urllib.parse
import gc
from PIL import Image
from gsbl.stick_bug import StickBug
import aiofiles
image_types = ["png", "jpeg", "gif", "jpg"]
import requests

class stickbug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="stickbug")
    async def command_cog(self, ctx):
        await ctx.send("Processing, please wait...")
        try:
            attachment_url = ctx.message.attachments[0].url
            file_request = requests.get(attachment_url)
            path = urllib.parse.urlparse(attachment_url).path
            ext = os.path.splitext(path)[1]
            open(f'stick{ext}', 'wb').write(file_request.content)
            sb = StickBug(Image.open(f"stick{ext}"))
            sb.video_resolution = (720, 720)
            sb.lsd_scale = 0.5
            video = sb.video  # MoviePy VideoClip
            sb.save_video("export.mp4") # last line of use
            '''
            for attachment in ctx.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    await attachment.save(attachment.filename)
            '''
            await ctx.send(f"<@{ctx.author.id}>, uploading the file...")
            with open(f'export.mp4', 'rb') as fp:
                await ctx.send(file=discord.File(fp, f'export.mp4'))
            os.remove(f"export.mp4")
            os.remove(f"stick{ext}")
            gc.collect()
        except Exception as e:
            print(e)
            await ctx.send("An error occurred.")

def setup(client):
    client.add_cog(stickbug(client))
