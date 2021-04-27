import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class slash_ghostping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ghostping", description="Ghostping a message/user.")
    @commands.has_permissions(administrator=True)
    async def ghostping(self, ctx, *, text):
        if ctx.author.guild_permissions.administrator:
            message = ctx.message
            await message.delete()
        else:
            await ctx.channel.send("You don't have permission for that command, Duh Doy!")
def setup(client):
    client.add_cog(slash_ghostping(client))