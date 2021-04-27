import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash_help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="help", description="View help info.")
    async def slash_help(self,ctx):
            await ctx.channel.send("This is a bot made by MrRazamataz. For help with the minecraft server look at <#698580298182688809> or do /help on the Minecraft Server.")
            await ctx.channel.send("For help with the bot please do raz!cmds or raz!docs.")
def setup(client):
    client.add_cog(slash_help(client))