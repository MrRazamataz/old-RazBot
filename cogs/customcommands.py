# MrRazamataz's RazBot
# Custom commands manager
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import json



class customcommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="cc")
    async def cc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You can `create` or `del`.")

    @cc.command()
    @commands.has_permissions(manage_guild=True)
    async def create(self, ctx, name, *, text):
        global cc
        save = {
            "text": f"{text}"
        }
        with open('customcommands.json', 'r+') as f:
            data = json.load(f)
            f.seek(0)
            f.truncate(0)
            data[f'{ctx.guild.id}-{name.lower()}'] = {"text": f"{text}"}
            json.dump(data, f, indent=4)
        await ctx.send(f"Added custom command with `{name.lower()}` which contains `{text}`.")
        with open("customcommands.json") as f:
            cc = json.load(f)
    @cc.command(name="delete", aliases=["remove", "del"])
    @commands.has_permissions(manage_guild=True)
    async def delete(self, ctx, name):
        global cc
        check = f"{ctx.guild.id}-{name.lower()}"
        with open('customcommands.json', 'r+') as f:
            data = json.load(f)
            try:
                data.pop(f"{check}")
            except Exception as e:
                await ctx.send(f"`{name.lower()}` was not found in the server's custom commands.")
                return
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)
        with open("customcommands.json") as f:
            cc = json.load(f)
        await ctx.send(f"Deleted `{name}`.")
    @cc.command()
    async def reload(self, ctx):
        global cc
        with open("customcommands.json") as f:
            cc = json.load(f)
        await ctx.send("Reloaded custom commands.")
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading custom commands...")
        global cc
        with open("customcommands.json") as f:
            cc = json.load(f)

    @commands.Cog.listener()
    async def on_message(self, message):
        global cc
        if message.guild is None:
            return
        guildid = str(message.guild.id)
        check = f"{guildid}-{message.content.lower()}"
        try:
            if check in cc:
                await message.channel.send(f'{cc[f"{check}"]["text"]}')
                #await message.channel.send(f'{cc[f"{check}"]}')
        except Exception as e:
            print(e)
def setup(client):
    client.add_cog(customcommands(client))
