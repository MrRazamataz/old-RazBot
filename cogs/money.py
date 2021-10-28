# MrRazamataz's RazBot
# bal cog
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import json
from discord.ext import tasks
class money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global moneydata
        print("Loading money...")
        with open("money.json") as f:
            moneydata = json.load(f)
        print("Starting save tasks loop...")
        self.save.start()
        global recent_change
        recent_change = False
    @commands.Cog.listener()
    async def on_message(self, message):
        global moneydata
        if message.guild is None:
            return
        if not message.author.bot:
            id = str(message.author.id)
            moneydata[id] = moneydata.get(id, 0) + 1
            print(f"Money for {id} has been increased by 1!")
            global recent_change
            recent_change = True


    @commands.command(name='bal', aliases=['balance'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        global moneydata, selfmessage
        selfmessage = "not set"
        if user == None:
            user = ctx.author
            selfmessage = "no"
        #id = ctx.message.author.id
        id = str(user.id)
        currentdata = []
        try:
            if selfmessage == "no":
                await ctx.send(f"Your bal is: `{moneydata[id]}`.")
            else:
                await ctx.send(f"{user.display_name}'s bal is: `{moneydata[id]}`.")
        except Exception as e:
            print(e)
    @balance.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are on a cooldown of that command for {error.retry_after:.2f}s!", delete_after=2)
    @commands.command(name='save')
    async def savebal(self, ctx):
        if ctx.author.id == 611976655619227648:
            with open("money.json", "w") as f:
                json.dump(moneydata, f, indent=4)
            await ctx.send("Saved.")
        else:
            await ctx.send("This command can only be used by MrRazamataz.")
    @tasks.loop(minutes=5)
    async def save(self):
        global recent_change
        if recent_change is True:
            with open("money.json", "w") as f:
                json.dump(moneydata, f, indent=4)
            print("Saved money from ram.")
            recent_change = False
        else:
            print("There are no recent changes to the money, not saving.")
def setup(client):
    client.add_cog(money(client))
