import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import asyncio
class slash_ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ban", description="Ban a user from this server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, arg1, reason=None):
        await member.send(f"You have been banned from `{member.guild.name}`. Ban reason: `{arg1}`")
        await member.ban(reason=arg1)
        await ctx.send(f"{member.name} has been banned by `{ctx.author.name}`, with the reason `{arg1}`!")
        await ctx.message.add_reaction("👍")
        await asyncio.sleep(2)
        await ctx.message.remove_reaction("👍", ctx.guild.me)

    #@commands.Cog.listener()
    #async def on_command_error(self, payload,ctx,error):
        #if isinstance(error, commands.MissingPermissions):
            #await ctx.send("You don't have permission to run this command, Duh-Doy!")
        #else:
            #await ctx.send("You don't have permission to run this command, Duh-Doy!")
            #print("raise error")

def setup(client):
    client.add_cog(slash_ban(client))