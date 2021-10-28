# MrRazamataz's RazBot
# misc commands
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import traceback

class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="reload", description="Reload all/one of the bots cogs!")
    async def reload(self, ctx, cog=None):
        if ctx.author.id == 611976655619227648:
            if not cog:
                # No cog, means we reload all cogs
                async with ctx.typing():
                    embed = discord.Embed(
                        title="RazBot Admin System:",
                        color=0x808080,
                        timestamp=ctx.message.created_at
                    )
                    for ext in os.listdir("./cogs/"):
                        if ext.endswith(".py") and not ext.startswith("_"):
                            try:
                                self.client.unload_extension(f"cogs.{ext[:-3]}")
                                self.client.load_extension(f"cogs.{ext[:-3]}")
                                embed.add_field(
                                    name=f"Reloaded: `{ext}`",
                                    value='\uFEFF',
                                    inline=False
                                )
                            except Exception as e:
                                embed.add_field(
                                    name=f"Failed to reload: `{ext}`",
                                    value=f"{e}",
                                    inline=False
                                )
                            await asyncio.sleep(0.5)
                    await ctx.send(embed=embed)
            else:
                # reload the specific cog
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Reloading all cogs!",
                        color=0x808080,
                        timestamp=ctx.message.created_at
                    )
                    ext = f"{cog.lower()}.py"
                    if not os.path.exists(f"./cogs/{ext}"):
                        # if the file does not exist
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value="This cog does not exist.",
                            inline=False
                        )

                    elif ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.client.unload_extension(f"cogs.{ext[:-3]}")
                            self.client.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:
                            desired_trace = traceback.format_exc()
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=desired_trace,
                                inline=False
                            )
                    await ctx.send(embed=embed)
                    if cog == "automod":
                        await ctx.send("raz!reloadvarforautomod")
                        await asyncio.sleep(1)
                        await ctx.delete()
                    if cog == "logs":
                        await ctx.send("raz!reloadvarforlogs")
                        await asyncio.sleep(1)
                        await ctx.delete()
                    if cog == "money":
                        await ctx.send("raz!reloadvarformoney")
                        await asyncio.sleep(1)
                        await ctx.delete()
        else:
            await ctx.send("This command can only be used by MrRazamataz.")

def setup(client):
    client.add_cog(misc(client))
