import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash_info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="info", description="Gives info on RazBot")
    async def slash_info(self,ctx):
        await ctx.channel.send("Hi! I am RazBot, a Discord bot written in python by MrRazamataz! I am meant for helping out around the KC Discord sevrer whilst also having fun with the great community! You can download my source code/view more info at https://mrrazamataz.ga/archive/razbot . You can even add me to your server there!")
def setup(client):
    client.add_cog(slash_info(client))