#MrRazamataz's RazBot

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os


client = commands.Bot(command_prefix="raz!", help_command=None)
cogs = ['cogs.mod', 'cogs.help', 'cogs.ping', 'cogs.lucky', 'cogs.countdown', 'cogs.ver', 'cogs.tps', 'cogs.spam', 'cogs.info', 'cogs.plugins', 'cogs.5minchannel', 'cogs.slowmode', 'cogs.kick', 'cogs.ban', 'cogs.unban', 'cogs.tempmute', 'cogs.mute', 'cogs.unmute', 'cogs.kcwelcome', 'cogs.permlist', 'cogs.tias', 'cogs.say', 'cogs.clear', 'cogs.ghostping', 'cogs.lockdown', 'cogs.unlock']
@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(activity=discord.Game(name='Starting...'))
    for cog in cogs: # Looks for the cogs,
        client.load_extension(cog) # Loads the cogs.
        print("Loaded cog")

    while True:
        print("Changed message")
        print (discord.__version__)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.users)} Members'))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='RazBot > ZacBot'))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='ReadyPlayerOne'))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Tears for Fears - Everybody wants to rule the world'))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='my creators website where you can download me! razbot.uk.to'))


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
banned_word_list = ["cunt","Cunt","卐"]


@client.event
async def on_message(message):
    if not message.guild:
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
    for word in razapinglistener:
        if word in message.content:
            await message.channel.send("You have pinged MrRazamataz, he will respond when he gets the chance. Please bear in mind that his timezone is GMT. He reads all ping messages so there is no need to spam ping.", delete_after=5)
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

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please make sure to say all required arguments (ERROR:MissingRequiredArgument). ")

client.run("TOKEN")
