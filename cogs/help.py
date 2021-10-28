# MrRazamataz's RazBot
# Help command
import discord
from discord import reaction
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="help")
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("__This is the RazBot help menu:__ \n\n`<>` = required input \n`()` = optional input \n✅ = "
                           "you have perms to use this command \n❌ = you don't have perms to use this command "
                           "\n\nYou can query a sub-section with `raz!help <query>`. \n__Valid queries are:__ "
                           "\n\n`music`, shows music commands. \n`mod`, shows the moderation commands. \n`tools`, "
                           "shows tools and useful commands. \n`logs`, shows logs settings \n`fun`, shows fun "
                           "commands.")


    @help.command()
    async def music(self, ctx):
        await ctx.send("Looking up perms...", delete_after=0.5)
        await ctx.send("__RazBot music commands:__ \n\n**Play:** `raz!p <song name or YouTube song/playlist URL>`, "
                       "plays the "
                       "song/playlist. \n**Pause:** `raz!pause` to pause then `raz!p` to unpause. \n**Skip:** "
                       "`raz!skip`, skip to the next "
                       "track in queue. \n**Back:**`raz!back`, go back to the last song in queue. \n**Queue:** `raz!q "
                       "(int, queue length "
                       "defaults to 10)`, shows the queue. "
                       "\n**Now playing:** `raz!np`, shows info about the currently playing song. \n**Shuffle:** "
                       "`raz!shuffle`, shuffles the queue "
                       "order. \n**Volume:** `raz!vol <0-150%>`, change the volume from 0-150%. \n**Replay:** "
                       "`raz!replay`, replay the "
                       "song.\n**Jump:** `raz!jump <time in s>`, jump to a specific timestamp in the song. "
                       "\n**Stop:** `raz!stop`, "
                       "stop the playing "
                       "track and clear queue. \n**Loop**: `raz!loop <all/1/none>`, loop with the selected mode. "
                       "\n**Lyrics:** `raz!lyrics`, "
                       "attempt to find "
                       "the lyrics to the playing song. \n**Skipto:** `raz!skipto`, skips to a song value that's in "
                       "the queue. "
                       "\n`<--- End --->`")
    @help.command()
    async def mod(self, ctx):
        await ctx.send("Looking up perms...", delete_after=0.5)
        if ctx.author.guild_permissions.manage_messages == True:
            message_emoji = "✅"
        else:
            message_emoji = "❌"
        if ctx.author.guild_permissions.ban_members == True:
            ban_emoji = "✅"
        else:
            ban_emoji = "❌"
        if ctx.author.guild_permissions.kick_members == True:
            kick_emoji = "✅"
        else:
            kick_emoji = "❌"
        if ctx.author.guild_permissions.manage_channels == True:
            channels_emoji = "✅"
        else:
            channels_emoji = "❌"
        if ctx.author.guild_permissions.mute_members == True:
            mute_emoji = "✅"
        else:
            mute_emoji = "❌"
        await ctx.send(f"__RazBot moderation commands:__ \n\n**Ban:** `raz!ban <user> (reason)`, bans the specified "
                       f"user from the server. {ban_emoji} \n**Unban:** `raz!unban <user>`, unbans the specified user from the "
                       f"server. {ban_emoji} \n**Mute:** `raz!mute <user>`, adds the muted role to the user. {ban_emoji} \n**Unmute:** "
                       f"`raz!unmute <user>`, removes the muted role from the user. {ban_emoji} \n**Temp Mute:** `raz!tempmute "
                       "<user> <Number> <s/m/h/d>`, tempmute the user for the amount of time specified. *Note: "
                       f"The space < > between <Number> and <s/m/h/d> is required.* {ban_emoji} \n**Kick:** `raz!kick <user>`, "
                       f"kicks the specified user from the server. {kick_emoji} \n**Clear:** `raz!clear <number>`, clears the "
                       f"specified amount of messages. {message_emoji} \n**Lockdown:** `raz!lockdown`, locks down the channel for non "
                       f"admins/staff. {channels_emoji} \n**Unlock:** `raz!unlock`, unlock-downs the channel after a raz!lockdown. {channels_emoji}"
                       "\n**Slowmode:** `raz!slowmode <int>`, puts the channel in slowmode for the specified amount, "
                       f"set to 0 to disable slowmode. {mute_emoji} \n**Warn:** `raz!warn <user> <reason>`, add a warning to the "
                       f"user in that server. {kick_emoji} \n**View Warnings:** `raz!warnings <user>`, view the warnings of the "
                       f"user for that server. {kick_emoji} \n`<--- End --->`")
    @help.command()
    async def tools(self, ctx):
        await ctx.send("Looking up perms...", delete_after=0.5)
        if ctx.author.guild_permissions.administrator == True:
            admin_emoji = "✅"
        else:
            admin_emoji = "❌"
        if ctx.author.guild_permissions.manage_guild == True:
            manage_emoji = "✅"
        else:
            manage_emoji = "❌"
        await ctx.send("__RazBot tools and useful commands:__ \n\n**Add Reaction Role:** `raz!set_reaction <RoleName> "
                       "<MessageID> <Emoji>`, adds a reaction which users can react to to give themselves the "
                       f"specified role (works multiple times on the same message with different reactions). {admin_emoji} \n**Add "
                       f"Role:** `raz!add_role <user> <role name>`, gives the user the role specified. {admin_emoji} \n~~**Lucky ( "
                       "Giveaway):** `raz!lucky (msg)`, adds a reaction and after 24 hours, picks a random person "
                       f"from the reactions.~~ Outdated, use new giveaway command below. {admin_emoji} \n**Wiki:** "
                       f"`raz!wiki <search term>`, searches Wikipedia "
                       f"for an article "
                       "matching your term. If the article fits in the Discord character limit, it will send an embed "
                       "with it in. If its too big, it will send the article link. If it can't find article it will "
                       "report back not found. \n**yt2mp3:** `raz!yt2mp3 <yt link>`, will take the YouTube link you "
                       "provided and convert it to a `.mp3` file then will send it. \n**Server info:** "
                       "`raz!serverinfo`, shows info about the current guild. \n**User info:** `raz!userinfo (@user "
                       "or ID)`, shows infomation on the user, or yourself if no user is specified. \n**Start "
                       "Giveaway:** `raz!gstart <emoji> <giveaway description>`, starts a giveaway in the server. Adds "
                       f"the emoji as a reaction to react to. {manage_emoji} \n**End Giveaway:** `raz!gend`, ends the active "
                       f"giveaway in a server. Picks random user from the reaction added. {manage_emoji}\n`<--- End "
                       "--->`")
    @help.command()
    async def logs(self, ctx):
        await ctx.send("Looking up perms...", delete_after=0.5)
        if ctx.author.guild_permissions.administrator == True:
            admin_emoji = "✅"
        else:
            admin_emoji = "❌"
        await ctx.send("__RazBot logs:__ \nBy default, all channels are logged into `#razbot-logs` if the "
                       "`#razbot-logs` channel exists. These commands can disable the logs in certain channels. "
                       "\n\n**Logs off:** `raz!log off <#channelmention>` \n**Logs on:** `raz!log on "
                       f"<#chnnelmention>`, to be used after a logs off command if you want them back on. \n{admin_emoji}")
    @help.command()
    async def fun(self, ctx):
        await ctx.send("__RazBot fun commands:__ \n\n**Wiki:** `raz!wiki <search term>`, searches Wikipedia for an "
                       "article matching your term. If the article fits in the Discord character limit, it will send "
                       "an embed with it in. If its too big, it will send the article link. If it can't find article "
                       "it will report back not found. \n**Meme:** `raz!meme`, sends a meme from Reddit using a "
                       "custom aiohttp request. \n**Bri'ish:** `raz!british`, same as Meme, but sends a post from a "
                       "meme british subreddit instead. \n*Beta Release* **Bal:** `raz!bal (user)`, shows your bal or "
                       "the user-pinged's bal. Bal is how many messages you have sent in servers with "
                       "RazBot.\n**Stick Bug:** `raz!stickbug "
                       "<picture attachement>`, converts the picture you send to a stick bug meme video. \n**Gay:** "
                       "`raz!gay (@user)`, makes the profile of whoever, like a rainbow, which makes it gay "
                       "apparently? "
                       "\n**Wasted:** `raz!wasted ( "
                       "@user)`, overlays the PFP with the wasted meme. \n**YouTube Comment:** `raz!youtube (@user) "
                       "<comment>`, will create a picture that looks like a YouTube comment, with the profile of the "
                       "user, and the message as the comment. \n`<--- End --->` ")
def setup(client):
    client.add_cog(help(client))
