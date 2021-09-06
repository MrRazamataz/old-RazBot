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
#This is where server intents is needed in the discord deveoper portal, this will be noted later on using the #Intents <desc> comment that is added by me. 
intents = discord.Intents.default()
intents.members = True
quotation_mark = '"'
client = commands.Bot(command_prefix="raz!", help_command=None, intents=intents, case_insensitive=True) #intents end
slash = SlashCommand(client, override_type=True, sync_commands=True)
client.warnings = {}
cogs = ['cogs.mod', 'cogs.help', 'cogs.ping', 'cogs.lucky', 'cogs.countdown', 'cogs.ver', 'cogs.tps', 'cogs.spam', 'cogs.info', 'cogs.plugins', 'cogs.5minchannel', 'cogs.slowmode', 'cogs.kick', 'cogs.ban', 'cogs.unban', 'cogs.tempmute', 'cogs.mute', 'cogs.unmute', 'cogs.kcwelcome', 'cogs.permlist', 'cogs.tias', 'cogs.say', 'cogs.clear', 'cogs.ghostping', 'cogs.lockdown', 'cogs.unlock', 'cogs.quotes', 'cogs.add_role', 'cogs.slash_add_role', 'cogs.slash_ban', 'cogs.slash_clear', 'cogs.slash_countdown', 'cogs.slash_ghostping', 'cogs.slash_help', 'cogs.slash_info', 'cogs.slash_kick', 'cogs.slash_lockdown', 'cogs.cmds', 'cogs.suggest', 'cogs.vote', 'cogs.user', 'cogs.meme'] # cogs.join_and_leave
client.reaction_roles = []
dm_list = []
for cog in cogs:  # Looks for the cogs,
    client.load_extension(cog)  # Loads the cogs.
    print("Loaded cog")
@client.event
async def on_ready():
    global uptime_start
    uptime_start = time.time()
    print("Ready")
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
    # while True:
    #     print("Changed message")
    #     print (discord.__version__)
    #     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='RazBot, thats me!'))
    #     await asyncio.sleep(30)
    #     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.users)} Members'))#Intents needed (server member) otherwise will show 1
    #     await asyncio.sleep(30)
    #     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='RazBot > ZacBot'))
    #     await asyncio.sleep(30)
    #     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='ReadyPlayerOne'))
    #     await asyncio.sleep(30)
    #     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='my new features getting coded!'))
    #     await asyncio.sleep(30)
    #     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='my creators website where you can download me! razbot.uk.to'))
    #     await asyncio.sleep(30)
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
async def update_totals(member):
    invites = await member.guild.invites()

    c = datetime.today().strftime("%Y-%m-%d").split("-")
    c_y = int(c[0])
    c_m = int(c[1])
    c_d = int(c[2])

    async with client.db.execute("SELECT id, uses FROM invites WHERE guild_id = ?",(member.guild.id,)) as cursor:  # this gets the old invite counts
        async for invite_id, old_uses in cursor:
            for invite in invites:
                if invite.id == invite_id and invite.uses - old_uses > 0:  # the count has been updated, invite is the invite that member joined by
                    if not (
                            c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7):  # year can only be less or equal, month can only be less or equal, then check days
                        print(invite.id)
                        await client.db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND id = ?",(invite.guild.id, invite.id))
                        await client.db.execute("INSERT OR IGNORE INTO joined (guild_id, inviter_id, joiner_id) VALUES (?,?,?)",(invite.guild.id, invite.inviter.id, member.id))
                        await client.db.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?",(invite.guild.id, invite.inviter.id))

                    else:
                        await client.db.execute("UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? and inviter_id = ?",(invite.guild.id, invite.inviter.id))

                    return

#invite manager
@client.event
async def on_member_join(member):
    await update_totals(member)
    await client.db.commit()


@client.event
async def on_member_remove(member):
    cur = await client.db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? and joiner_id = ?",(member.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        return

    inviter = res[0]

    await client.db.execute("DELETE FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
    await client.db.execute("DELETE FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, member.id))
    await client.db.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (member.guild.id, inviter))
    await client.db.commit()


@client.event
async def on_invite_create(invite):
    await client.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)",
                         (invite.guild.id, invite.inviter.id, invite.uses, 0, 0))
    await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)",
                         (invite.guild.id, invite.id, invite.uses))
    await client.db.commit()


@client.event
async def on_invite_delete(invite):
    await client.db.execute("DELETE FROM invites WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
    await client.db.commit()


@client.event
async def on_guild_join(guild):  # add new invites to monitor
    for invite in await guild.invites():
        await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses), VAlUES (?,?,?)",
                             (guild.id, invite.id, invite.uses))

    await client.db.commit()


@client.event
async def on_guild_remove(guild):  # remove all instances of the given guild_id
    await client.db.execute("DELETE FROM totals WHERE guild_id = ?", (guild.id,))
    await client.db.execute("DELETE FROM invites WHERE guild_id = ?", (guild.id,))
    await client.db.execute("DELETE FROM joined WHERE guild_id = ?", (guild.id,))

    await client.db.commit()


# commands
@client.command()
async def invites(ctx, member: discord.Member = None):
    if member is None: member = ctx.author

    # get counts
    cur = await client.db.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?",
                               (ctx.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        normal, left, fake = 0, 0, 0

    else:
        normal, left, fake = res

    total = normal - (left + fake)

    em = discord.Embed(
        title=f"Invites for {member.name}#{member.discriminator}",
        description=f"{member.mention} currently has **{total}** invites. (**{normal}** normal, **{left}** left, **{fake}** fake).",
        colour=discord.Colour.orange())

    await ctx.send(embed=em)



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
        return await ctx.send("The member you provided (or didnt) could not be found, please make sure to @ mention them.")

    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

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


@client.command()
@commands.has_permissions(ban_members=True)
async def warnings(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("The member you provided (or didnt) could not be found, please make sure to @ mention them.")

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
    #for word in razapinglistener:
        #if word in message.content:
            #await message.channel.send("You have pinged MrRazamataz, he will respond when he gets the chance. Please bear in mind that his timezone is GMT. He reads all ping messages so there is no need to spam ping.", delete_after=5)
    if 611976655619227648 in [mention.id for mention in message.mentions]: #the numbers are my id (replace with someone else if you want)
        if not message.author.bot:
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇳")
            await message.add_reaction("🇬")
            await message.clear_reactions()
            print ("Ping warn sent (raza).")
    if 442243565494599701 in [mention.id for mention in message.mentions]: #here the number is zac
        if not message.author.bot:  #if message.author != client.user:
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇳")
            await message.add_reaction("🇬")
            await message.clear_reactions()
            print ("Ping warn sent (zac).")
    if 675643162374701056 in [mention.id for mention in message.mentions]: #here the number is lil
        if not message.author.bot:  #if message.author != client.user:
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇳")
            await message.add_reaction("🇬")
            await message.clear_reactions()
            print ("Ping warn sent (lil).")
    if 730474271352291438 in [mention.id for mention in message.mentions]: #here the number is tiger
        if not message.author.bot:  #if message.author != client.user:
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇳")
            await message.add_reaction("🇬")
            await message.clear_reactions()
            print ("Ping warn sent (Tiger).")
    if 807587465720102962 in [mention.id for mention in message.mentions]: #here the number is chewie
        if not message.author.bot:  #if message.author != client.user:
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇳")
            await message.add_reaction("🇬")
            await message.clear_reactions()
            print ("Ping warn sent (chewie).")
    if 649681762598912010 in [mention.id for mention in message.mentions]: #here the number is phaontom
        if not message.author.bot:  #if message.author != client.user:
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇳")
            await message.add_reaction("🇬")
            await message.clear_reactions()
            print ("Ping warn sent (phantom).")
    guild = message.guild
    log_channel = discord.utils.get(guild.channels, name="razbot-logs")
    if log_channel is None:
        await client.process_commands(message)
        return
    if not message.author.bot:
        embed = discord.Embed(
            color=0xffd700,
            timestamp=datetime.utcnow(),
            description="in {}:\n{}".format(message.channel.mention, message.content)
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text=message.author.id)
        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        await log_channel.send(embed=embed)

    await client.process_commands(message)


#Proper commands here
@client.command(name="hello")
async def hello_world(ctx: commands.Context):
    await ctx.send("Hello, world!")

@client.command(name="ping-test")
async def command_pingtest(ctx: commands.Context):
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")



#Testing below, not to be used.

@client.command(name="bug.report")
async def command_bugreport(ctx: commands.Context):
    await ctx.send("BugReport sequence starting!")
    await ctx.send("What software are you playing on (bedrock or java)? Please say your answer in lowercase.")
    device = await client.wait_for('message')
    if device.content == "bedrock":
        await ctx.send("You selected bedrock!")
        await ctx.send("Whats the bug you are reporting?")
        bedrock_bug = await client.wait_for('message')
        await ctx.send ("Listening...")
        if bedrock_bug.content == on_message:
             await ctx.send(bedrock_bug)


    elif device.content == "java":
        await ctx.send("You selected java!")
        await ctx.send("What software are you playing on (bedrock or java)? Please say your answer in lowercase.")

xbox = "⊠ "
box = "▢ "
to_do = []
check_list = [box, box, box, box]
# check_list = ["▢ ", "▢ ", "▢ ", "▢ "]

@client.command(name="bug.check")
async def check(ctx, x):

    if check_list[int(x)-1] == box:
        check_list[int(x)-1] = xbox
    else:
        check_list[int(x)-1] = box
    await list(ctx)
@client.command(name="bug.list")
async def list(ctx):
    for i in range (len(to_do)):
        bugdata = (check_list[i], to_do[i])
        f = open("bug_data.txt", "r")
        await ctx.send(f.read())
@client.command(name="bug.listnum")
async def list_number(ctx):
    for i in range (len(to_do)):
        ligne = i+1
        bugdata = (ligne, check_list[i], to_do[i])
        await ctx.send(bugdata)
@client.command(name="bug.create")
async def create(ctx, x):
    to_do.append(x)
    check_list.append("▢ ")
    await list(ctx)
    f = open("bug_data.txt.txt", "a")
    f.write(list)
    f.write("\n")
@client.command(name="bug.remove")
async def remove(ctx, x):
    to_do.pop(int(x)-1)
    check_list.pop(int(x)-1)
    await list(ctx)





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
        await ctx.send("Unkown command, sorry. Use `raz!cmds` to view a list of commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")


async def setup():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("inviteData.db")
    await client.db.execute("CREATE TABLE IF NOT EXISTS totals (guild_id int, inviter_id int, normal int, left int, fake int, PRIMARY KEY (guild_id, inviter_id))")
    await client.db.execute("CREATE TABLE IF NOT EXISTS invites (guild_id int, id string, uses int, PRIMARY KEY (guild_id, id))")
    await client.db.execute("CREATE TABLE IF NOT EXISTS joined (guild_id int, inviter_id int, joiner_id int, PRIMARY KEY (guild_id, inviter_id, joiner_id))")

    # fill invites if not there
    for guild in client.guilds:
        for invite in await guild.invites():  # invites before bot was added won't be recorded, invitemanager/tracker don't do this
            await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)",(invite.guild.id, invite.id, invite.uses))
            await client.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)",(guild.id, invite.inviter.id, 0, 0, 0))

    await client.db.commit()
client.loop.create_task(setup())
client.run("Nzk5MjI4NjI4MTA1MTY2ODQ4.YAAhqQ.f-5lXZg74qE673KjqTOT7FnayhQ")
asyncio.run(client.db.close())