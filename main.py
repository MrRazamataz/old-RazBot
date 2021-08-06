#MrRazamataz's RazBot

import random
import discord, datetime, time
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import time
from discord_slash import SlashCommand, SlashContext
import aiosqlite
from datetime import datetime
from discord.utils import get
#This is where server intents is needed in the discord deveoper portal, this will be noted later on using the #Intents <desc> comment that is added by me.
intents = discord.Intents.default()
intents.members = True
quotation_mark = '"'
client = commands.Bot(command_prefix="raz!", help_command=None, intents=intents, case_insensitive=True) #intents end
slash = SlashCommand(client, override_type=True, sync_commands=True)
client.warnings = {}
cogs = ['cogs.mod', 'cogs.help', 'cogs.ping', 'cogs.lucky', 'cogs.countdown', 'cogs.ver', 'cogs.tps', 'cogs.spam', 'cogs.info', 'cogs.plugins', 'cogs.5minchannel', 'cogs.slowmode', 'cogs.kick', 'cogs.ban', 'cogs.unban', 'cogs.tempmute', 'cogs.mute', 'cogs.unmute', 'cogs.kcwelcome', 'cogs.permlist', 'cogs.tias', 'cogs.say', 'cogs.clear', 'cogs.ghostping', 'cogs.lockdown', 'cogs.unlock', 'cogs.quotes', 'cogs.add_role', 'cogs.slash_add_role', 'cogs.slash_ban', 'cogs.slash_clear', 'cogs.slash_countdown', 'cogs.slash_ghostping', 'cogs.slash_help', 'cogs.slash_info', 'cogs.slash_kick', 'cogs.slash_lockdown', 'cogs.cmds', 'cogs.suggest', 'cogs.vote', 'cogs.user', 'cogs.meme', 'cogs.british', 'cogs.wiki', 'cogs.music'] # cogs.join_and_leave
client.reaction_roles = []
dm_list = []
for cog in cogs:  # Looks for the cogs,
    client.load_extension(cog)  # Loads the cogs.
    print("[RazBot] Loaded cog")
#for file in os.listdir('cogs'):
       # if file.endswith('.py'):
            #try:
                #client.load_extension("cogs." + os.path.splitext(file)[0])
                #print(f'Extension {file} loaded.')
            #except Exception as e:
                #print(f'Failed to load cog{file}: {e}')
@client.event
async def on_ready():
    global uptime_start
    uptime_start = time.time()
    print("[RazBot] Loading...")
    for guild in client.guilds:
        client.warnings[guild.id] = {}

        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]

    print(client.user.name + " is ready.")
    async with aiofiles.open("dm.txt", mode="a") as temp:
        pass

    #async with aiofiles.open("dm.txt", mode="r") as file:
        #lines = await file.readlines()
        #for line in lines:
            #dm_list.append((int(data[0])))

    async with aiofiles.open("reaction_roles.txt", mode="a") as temp:
        pass

    async with aiofiles.open("reaction_roles.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))
    print(f"{client.user.name} is ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.users)} Members, razbot.uk.to'))
    while True:
        await asyncio.sleep(10)
        if os.path.getsize("spam_detect.txt") > 0:
            with open("spam_detect.txt", "r+") as file:
                file.truncate(0)
            print("Cleared spam detect text file.")
        else:
            print("Spam file was empty, so not clearing.")
def check_if_string_in_file(file_name, string_to_search): #string checker
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False
@client.event
async def on_member_join(member):
    print("Status updated, user joined.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f'{len(client.users)} Members, razbot.uk.to. Newest member is `{member.name}`!'))
@client.command(name="bugreport")
async def command_cog(ctx, *, message):
    async with aiofiles.open("bug_data.txt", mode="a") as file:
        await file.write(f"`{message}`, reported by `{ctx.author}`." + "\n")
        await file.close()
        await ctx.send("Bug report has been saved.")


@client.command(name="bugreport.list")
async def dm_all(ctx):
    await ctx.send("Reading bug reports from file:")
    bugreportlist = "Empty!"
    async with aiofiles.open("bug_data.txt", mode="r") as bugreportlist:
        count = 0
        async for line in bugreportlist:
            count += 1
            #print("Line{}: {}".format(count, line.strip()))
            await ctx.send(f"Line {count}: {line}")

@client.command(name="set_status.watch")
async def set_status_watch(ctx, status_text):
    if ctx.author.id == 611976655619227648:
        message = ctx.message
        status_output = quotation_mark + status_text + quotation_mark
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_text))
        await ctx.send(f"Status set to: `{status_output}`")
        print(f"Status Changed to {status_output}.")
    else:
        await ctx.send("This command can only be ran by MrRazamataz!")
@client.command(name="set_status.listen")
async def set_status_listen(ctx, status_text):
    if ctx.author.id == 611976655619227648:
        message = ctx.message
        status_output = quotation_mark + status_text + quotation_mark
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_text))
        await ctx.send(f"Status set to: `{status_output}`")
        print(f"Status Changed to {status_output}.")
    else:
        await ctx.send("This command can only be ran by MrRazamataz!")
@client.command(name="set_status.play")
async def set_status_play(ctx, status_text):
    if ctx.author.id == 611976655619227648:
        message = ctx.message
        status_output = quotation_mark + status_text + quotation_mark
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status_text))
        await ctx.send(f"Status set to: `{status_output}`")
        print(f"Status Changed to {status_output}.")
    else:
        await ctx.send("This command can only be ran by MrRazamataz!")
@client.command(name="set_status.reset")
async def set_status_reset(ctx):
    if ctx.author.id == 611976655619227648:
        message = ctx.message
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.users)} Members, razbot.uk.to'))
        await ctx.send("Status set to default.")
        print("Status set to default.")
    else:
        await ctx.send("This command can only be ran by MrRazamataz!")
@client.command(name="leaveserver")
async def leaveserver(ctx, guild_id):
    if ctx.author.id == 611976655619227648:
        await client.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left: {guild_id}")
    else:
        await ctx.send("This command can only be ran by MrRazamataz!")
@client.command(name="vcamount")
async def vcamount(ctx):
    count_list = []
    for vc in client.voice_clients:
        for member in vc.members:
            count_list.append(member)
    await ctx.send(f"There are {count_list} connected voice channels!")
# Reaction Role Code
@client.command()
@commands.has_permissions(administrator=True)
async def set_reaction(ctx, role: discord.Role = None, msg: discord.Message = None, emoji=None):
    if role != None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        client.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))

        async with aiofiles.open("reaction_roles.txt", mode="a") as file:
            emoji_utf = emoji.encode("utf-8")
            await file.write(f"{role.id} {msg.id} {emoji_utf}\n")

        await ctx.channel.send("Reaction has been set.")

    else:
        await ctx.send("Invalid arguments.")


@client.event
async def on_raw_reaction_add(payload):
    for role_id, msg_id, emoji in client.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            await payload.member.add_roles(client.get_guild(payload.guild_id).get_role(role_id))
            return

#This here needs the server members intent to detect that the user has removed the reaction.
@client.event
async def on_raw_reaction_remove(payload):
    for role_id, msg_id, emoji in client.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            guild = client.get_guild(payload.guild_id)
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
            return
@client.command(name="dm_in")
async def dm_in(ctx):
    if check_if_string_in_file('dm.txt', f"{ctx.message.author.id}\n"):
        await ctx.channel.send("You are already in DM notifications, thanks!")
    else:
        async with aiofiles.open("dm.txt", mode="a") as file:
            await file.write(f"{ctx.message.author.id}\n")
            await file.close()
        await ctx.channel.send("Added to DM notifications, thank you!")
@client.command(name="dm_all.in")
async def dm_all(ctx, *, text):
    if ctx.author.id == 611976655619227648:
        await ctx.send("DM messaging started, this may take a while depending on the amount of users to respect the discord API.")
        dm_list = []
        with open('dm.txt') as dm_file:
            for line in dm_file:
                try:
                    user = client.get_user(int(line))
                    await user.send(text)
                    await asyncio.sleep(5)
                except discord.Forbidden:
                    pass


        await ctx.send("DM message sent to everyone!")
    else:
        await ctx.send("This command can only be ran by MrRazamataz!")
command_pygood = ["Python is good"]
command_pybad = ["Python is bad"]
command_razaiscool = ["raza is cool"]
command_chewieiscool = ["chewie is cool"]
command_serverisdown = ["raz!server down", "server down"]
command_hello = ["Hi Razbot", "Hi Raz bot", "Hi RazBot"]
command_vote = ["raz!vote"]
command_suggest = ["raz!suggest"]
command_dab = ["/dab"]
command_hate = ["i hate u razbot", "i hate you razbot", "razbot bad", "razbot is bad", "shut up razbot", "SHUTUP RAZBOT"]
razapinglistener = ["<@611976655619227648>"]
banned_word_list = ["卐"]
#warn command
@client.event
async def on_guild_join(guild):
    client.warnings[guild.id] = {}



@client.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        return await ctx.send("Yo hold up there! You need to @ mention a user to warn them! \n `raz!warn <@member> [reason]` <--- format to follow.")

    if reason is None:
        return await ctx.send("Warning a user with no reason is kinda pointless, I think you should proivde a reason! \m `raz!warn <@member> [reason]` <--- format to follow (you got there mostly)!")

    try:
        first_warning = False
        client.warnings[ctx.guild.id][member.id][0] += 1
        client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = client.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{member.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")
    #await member.send(f"You have been warned in `{member.guild.name}`. Warn reason: `{reason}`. **Please make sure to follow the rules, otherwise you risk futher punishment!**")
    embed = discord.Embed(title=f"You have been warned in `{member.guild.name}`", description="", colour=discord.Colour.red())
    embed.description += f"You currently have **{count}** warnings in `{member.guild.name}`.\n Your latest warning had the reason: `{reason}`.\n Please make sure to follow the rules, otherwise you may risk further punishment!"
    await member.send(embed=embed)
@client.command()
@commands.has_permissions(ban_members=True)
async def warnings(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("You didnt @ mention a user, so I don't know who to search for in my database! Duh-Doy! \n `raz!warnings <@member>`")

    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in client.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}:** It was given by {admin.mention} for *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError:  # no warnings
        await ctx.send("This user has no warnings.")
#message events
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.guild:
        if message.author == client.user:
            return
        else:
            await message.author.send("Hello there! Commands don't *yet* work in DM's, sorry about that. Please go to the discord server you want to run the commands in and run them there!")
            return
    for word in command_pybad:
        if word in message.content:
            await message.channel.send("You are wrong and you are bad. ")
            await message.add_reaction("❌")
            print("Message sent in chat.")
    for word in command_pygood:
        if word in message.content:
            await message.channel.send("You are great and correct.")
            await message.add_reaction("👍")
            await asyncio.sleep (5)
            await message.remove_reaction("👍", message.guild.me)
            print("Message sent in chat.")
    for word in command_razaiscool:
        if word in message.content:
            await message.channel.send("Raza is very very cool")
            await message.add_reaction("👍")
            await asyncio.sleep (5)
            await message.remove_reaction("👍", message.guild.me)
            print("Message sent in chat.")
    for word in command_chewieiscool:
        if word in message.content:
            await message.channel.send("But not as cool as raza.")
            await message.add_reaction("👍")
            await asyncio.sleep (5)
            await message.remove_reaction("👍", message.guild.me)
            print("Message sent in chat.")
    for word in command_serverisdown:
        if word in message.content:
            await message.channel.send("Contacting...")
            await message.add_reaction("👍")
            await asyncio.sleep(2)
            await message.remove_reaction("👍", message.guild.me)
            await message.channel.send("/tps")
            await message.channel.send("/playerlist")
            await asyncio.sleep(2)
            await message.channel.send("Did that do anything? If not ping MrRazamataz or Zaczer. The TPS should be near 20 if it's not lagging.")
            print("Server down message sent in chat.")
    for word in command_hello:
        if word in message.content:
            await message.channel.send("Hello there how are you?")
            #try:
                #message = await
            await asyncio.sleep(5)
            await message.channel.send("Thats cool to hear!")
            print("Message sent in chat.")
    for word in command_vote:
        if message.author.guild_permissions.administrator:
            if word in message.content:
                await message.add_reaction("<:upvote:707157967471902731>")
                await message.add_reaction("<:Downvote:707158001496096808>")
                await message.channel.send("React with <:upvote:707157967471902731> for yes.")
                await message.channel.send("React with <:Downvote:707158001496096808> for no.")
                await message.channel.send("*React on the message above my messages!*")
                print("Message sent in chat.")
    for word in command_suggest:
        if word in message.content:
            await message.add_reaction("<:upvote:707157967471902731>")
            await message.add_reaction("<:Downvote:707158001496096808>")
            print("Message sent in chat.")
    for word in command_dab:
        if word in message.content:
            await message.channel.send("ヽ(o⌣oヾ)")
            await message.add_reaction("👍")
            await asyncio.sleep (5)
            await message.remove_reaction("👍", message.guild.me)
            print("Message sent in chat.")
    for word in command_hate:
        if word in message.content:
            await message.channel.send("Well thats not very nice, what have I ever done to you? How about a lesson in dms.?")
            await message.author.send("Hate is a very strong word.")
            await message.author.send("People can get very sad about this.")
            await message.author.send("If you are ever sad, please contact someone (MrRazamataz has his dms open).")
            await message.author.send("Have a nice day! Do you still hate me?")
            print("Hate dealt with.")
    for word in banned_word_list:
        if not message.author.bot:
            if word in message.content:
                await message.delete()
                print ("Deleted")
                await message.author.send("You just sent a banned word, please refrain from doing that again.")
                await message.author.send("https://mrrazamataz.ga/archive/mcserver/Code%20of%20conduct.png")
    if get(message.guild.roles, name="RazBot-Spam-Mute"):
        role = get(message.guild.roles, name="RazBot-Spam-Mute")
        counter = 0
        with open("spam_detect.txt", "r+") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter+=1
            file.writelines(f"{str(message.author.id)}\n")
            if counter > 5:
                await message.author.add_roles(role)
                embed = discord.Embed(title=f"You have been automatically temp-muted in `{message.guild.name}`", description="",
                                      colour=discord.Colour.red())
                embed.description += f"This was for spamming, and I, RazBot, picked up on it and muted you (the server owner has my spam mute turned on), sorry about that, but don't spam! \n This has been recorded in the RazBot logs."
                await message.author.send(embed=embed)
                guild = message.guild
                log_channel = discord.utils.get(guild.channels, name="razbot-logs")
                if log_channel is None:
                    await client.process_commands(message)
                    return
                else:
                    embed = discord.Embed(title="{} was auto temp-muted for spamming.".format(message.author.name),
                                          description="in {}:\n{}".format(message.channel.mention, message.content),
                                          color=0xff7700, timestamp=datetime.utcnow(), )
                    embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                    embed.set_footer(text=message.author.id)

                    embed.add_field(name="Action:", value="User has been temp-muted for 10 seconds.",
                                    inline=True)
                    await log_channel.send(embed=embed)
                await asyncio.sleep(10)
                await message.author.remove_roles(role)
        await client.process_commands(message)         #await client.process_commands(message)
    else:
        await client.process_commands(message)
        return

    #for word in razapinglistener:
        #if word in message.content:
            #await message.channel.send("You have pinged MrRazamataz, he will respond when he gets the chance. Please bear in mind that his timezone is GMT. He reads all ping messages so there is no need to spam ping.", delete_after=5)


    #await client.process_commands(message)
@client.event
async def on_message_delete(message):
    guild = message.guild
    log_channel = discord.utils.get(guild.channels, name="razbot-logs")
    if log_channel is None:
        await client.process_commands(message)
        return
    if not message.author.bot:
        if check_if_string_in_file('logsettings.txt', f"{message.channel.id}\n"):
            return
        else:
            embed = discord.Embed(title="{} deleted a message.".format(message.author.name),
                                  description="in {}:\n{}".format(message.channel.mention, message.content), color=0xFF0000, timestamp=datetime.utcnow(),)
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=message.author.id)

            embed.add_field(name="Action:", value="Message has been deleted by user.",
                            inline=True)
            await log_channel.send(embed=embed)
    await client.process_commands(message)
@client.event
async def on_message_edit(message_before, message_after):
    if check_if_string_in_file('logsettings.txt', f"{message_after.channel.id}\n"):
        return
    else:
        editEm=discord.Embed(title="Message edited".format(str(message_before.author)),
        description="", color=discord.Color.purple())
        editEm.add_field(name= "**Before:**" ,value=message_before.content, inline=False)
        editEm.add_field(name= "**After:**" ,value=message_after.content, inline=False)
        editEm.set_author(name=message_before.author, icon_url=message_before.author.avatar_url)
        editEm.timestamp = datetime.utcnow()
        log_channel = discord.utils.get(message_after.guild.channels, name="razbot-logs")
        if log_channel is None:
            return
        else:
            await log_channel.send(embed=editEm)
@client.command(name="log.off")
@commands.has_permissions(administrator=True)
async def logoff(ctx, channel: discord.TextChannel):
    if check_if_string_in_file('logsettings.txt', f"{channel.id}\n"):
        await ctx.channel.send("This channel already has logs disabled!")
    else:
        async with aiofiles.open("logsettings.txt", mode="a") as file:
            await file.write(f"{channel.id}"+ "\n")
            await file.close()
            await ctx.channel.send(f"{channel.mention} will no longer show in RazBot Logs.")
#Proper commands here
@client.command(name="hello")
async def hello_world(ctx: commands.Context):
    await ctx.send("Hello, world!")

@client.command(name="ping-test")
async def command_pingtest(ctx: commands.Context):
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(client.latency * 1000)}ms")




#Error handlers below
#@client.event
#async def on_command_error(ctx, error):
    #if isinstance(error, commands.MissingPermissions):
        #await ctx.send("You don't have permission to run this command, Duh-Doy!")
    #else:
        #raise error

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please make sure to say all required arguments (ERROR:MissingRequiredArgument). ")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unkown command, sorry. Use `raz!help` to view a list of commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")

client.run("TOKEN")
