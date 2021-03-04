#MrRazamataz's RazBot

import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix="raz!", help_command=None)

@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(activity=discord.Game(name='Starting...'))
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
@client.command(name="help")
async def command_help(ctx: commands.Context):
    await ctx.channel.send("This is a bot made by MrRazamataz. For help with the minecraft server look at <#698580298182688809> or do /help on the Minecraft Server.")
@client.command(name="ping")
async def command_ping(ctx: commands.Context):
    await ctx.channel.send("Pong!")
    await ctx.message.add_reaction("👍")
    await asyncio.sleep(5)
    await ctx.message.remove_reaction("👍", ctx.guild.me)
    print("Message sent in chat.")
@client.command(name="lucky")
async def command_lucky(ctx: commands.Context):
    if ctx.author.guild_permissions.administrator:
        m = await ctx.channel.send("OO yay a giveaway, my favourite thing to do. It's always fun to give back the epic community. Anyway, just react to the message with my reaction I have added and wait, it's as easy as that!")
        await m.add_reaction("👍")
        await asyncio.sleep(86400)
        await m.remove_reaction("👍", m.guild.me)
        m = await m.channel.fetch_message(m.id)
        member = random.choice(await m.reactions[0].users().flatten())
        await ctx.channel.send("The lucky winner is......")
        await asyncio.sleep(1)
        await ctx.channel.send("The")
        await asyncio.sleep(1)
        await ctx.channel.send("suspense")
        await asyncio.sleep(1)
        await ctx.channel.send("Here we go....")
        await asyncio.sleep(2)
        await ctx.channel.send(member.mention)
        await ctx.channel.send("You have won! How very lucky of you! :). Now wait for <@611976655619227648> to notice and he will give you your prize!")
        print("Message sent in chat.")
    else:
        await ctx.channel.send("It seems you have no perms to run `raz!lucky`!")
@client.command(name="ver")
async def command_ver(ctx: commands.Context):
    async with ctx.channel.typing():
        await asyncio.sleep(2)
        await ctx.channel.send("This version of the bot is running version 3.2, with some more moderation command and more things that have been fixed.")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("⚫")
        await ctx.message.add_reaction("2️⃣")
        print("Message sent in chat.")
@client.command(name="countdown")
async def command_countdown(ctx: commands.Context):
    await ctx.message.add_reaction("🔟")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("🔟", ctx.guild.me)
    await ctx.message.add_reaction("9️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("9️⃣", ctx.guild.me)
    await ctx.message.add_reaction("8️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("8️⃣", ctx.guild.me)
    await ctx.message.add_reaction("7️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("7️⃣", ctx.guild.me)
    await ctx.message.add_reaction("6️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("6️⃣", ctx.guild.me)
    await ctx.message.add_reaction("5️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("5️⃣", ctx.guild.me)
    await ctx.message.add_reaction("4️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("4️⃣", ctx.guild.me)
    await ctx.message.add_reaction("3️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("3️⃣", ctx.guild.me)
    await ctx.message.add_reaction("2️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("2️⃣", ctx.guild.me)
    await ctx.message.add_reaction("1️⃣")
    await asyncio.sleep(1)
    await ctx.message.remove_reaction("1️⃣", ctx.guild.me)
    await ctx.message.add_reaction("👍")
    await asyncio.sleep(5)
    await ctx.message.remove_reaction("👍", ctx.guild.me)
    print("Countdown run.")
@client.command(name="tps")
async def command_tps(ctx: commands.Context):
    await ctx.channel.send("/tps")
    print("TPS Done.")
@client.command(name="spam")
async def command_spam(ctx: commands.Context):
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Spam is bad don't you know! A dm lesson is needed here.")
        await ctx.author.send("Spamming is very annoying and getting a bot to spam for you is not only scummy, but also against Discord TOS.")
        print("Message sent in chat.")
@client.command(name="info")
async def command_info(ctx: commands.Context):
    await ctx.channel.send("Hi! I am RazBot, a Discord bot written in python by MrRazamataz! I am meant for helping out around the KC Discord sevrer whilst also having fun with the great community! You can download my source code/view more info at https://mrrazamataz.ga/archive/razbot . You can even add me to your server there!")
@client.command(name="plugins")
async def command_info(ctx: commands.Context):
    async with ctx.channel.typing():
        await asyncio.sleep(2)
        await ctx.channel.send("Yoo lemme get that help coming youuuuuur waaayyy!")
        async with ctx.channel.typing():
            await asyncio.sleep(2)
            embed = discord.Embed(title='KC Plugin Help page:',description="This is still a work in progress but here is what is planned to be used to get help with plugin commands on KC instead of just linking to a badly made html site. However, until that day comes here is the page for your plugin help.\n http://kingdomscrusade.net/plugins.html",color=0x00ff00)
            embed.set_image(url='https://mrrazamataz.ga/archive/RazBot.png')
            embed.set_footer(text='RazBot', icon_url='https://mrrazamataz.ga/archive/RazBot.png')
            await ctx.send(embed=embed)
@client.command(name="5minchannel")
async def command_tempchannel(ctx: commands.Context):
    if ctx.author.guild_permissions.administrator:
        await ctx.guild.create_text_channel('5min')
        await ctx.channel.send("The channel (#5min) will be deleted in 5 mins.")
        await asyncio.sleep (5)
        await ctx.guild.remove_text_channel('5min') #lol this doesnt work yet
    else:
        await ctx.channel.send("It seems you have no perms to run `raz!5minchannel`!")
@client.command(name="slowmode")
async def setdelay(ctx, seconds: int):
    if ctx.author.guild_permissions.mute_members:
        if seconds > 21600:
            await ctx.channel.send("Sorry, it has to be less than 21600 seconds!")
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
            print ("Slowmode setting changed.")
    else:
        await ctx.channel.send("It seems you have no perms to run `raz!slowmode`!")
@client.command(name="kick")
@commands.has_permissions(kick_members=True)

async def kick(ctx, member: discord.Member):

    await member.kick()
    await ctx.message.add_reaction("👍")
    await ctx.send(f"{member.name} has been kicked by {ctx.author.name}!")
    await ctx.author.send(f"You kicked {member.display_name}.")
    await ctx.message.remove_reaction("👍", ctx.guild.me)
#Ban (perm) command
@client.command(name="ban")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"{member.name} has been banned by {ctx.author.name}!")
    await ctx.message.add_reaction("👍")
    await asyncio.sleep (5)
    await ctx.message.remove_reaction("👍", ctx.guild.me)
#Unban Command
@client.command(name="unban")
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            await ctx.message.add_reaction("👍")
            await asyncio.sleep(5)
            await ctx.message.remove_reaction("👍", ctx.guild.me)
            return
#TempMute Command
#@client.command(name="tempmute", aliases=['mute'], pass_context = True)
@client.command(name="tempmute", pass_context = True)
@commands.has_permissions(ban_members = True)
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)

            embed = discord.Embed(title="RazBot Mute System:", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.dark_purple())
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Mute duration:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="RazBot Mute System: ", description=f"Unmuted (tempmute expired): -{member.mention} ", colour=discord.Colour.dark_purple())
            await ctx.send(embed=embed)

            return
#mute
@client.command(name="mute")
@commands.has_permissions(ban_members = True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            await ctx.channel.send("User has been muted.")

#Unmute
@client.command(name="unmute")
@commands.has_permissions(ban_members = True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            await ctx.channel.send("User has been unmuted.")


@client.command(name="kc.welcome")
async def command_kcwelcome(ctx: commands.Context):
    await ctx.message.delete()
    await ctx.channel.send("Hello there KC Bot! Im sure we can get along even though we understand different languages. Good luck in this community!")


@client.command(name="permlist")
async def command_permlist(ctx: commands.Context):
    await ctx.author.send("https://www.mrrazamataz.ga/archive/discord%20perms.png")
    await ctx.author.send("Taken from: https://discordpy.readthedocs.io/en/latest/api.html?highlight=permissions#discord.Permissions")
    await ctx.channel.send("You got mail!")
    await ctx.message.add_reaction("👍")
    await asyncio.sleep(5)
    await ctx.message.remove_reaction("👍", ctx.guild.me)
    print("Permlist command ran")

@client.command(name="ping-test")
async def command_pingtest(ctx: commands.Context):
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")
@client.command(name="tias")
async def command_tias(ctx: commands.Context):
    await ctx.channel.send("https://tryitands.ee/")
@client.command(name="say")
async def say(ctx, *, text):
    if ctx.author.guild_permissions.administrator:
        message = ctx.message
        await message.delete()
        await ctx.send(f"{text}")
    else:
        message = ctx.message
        await message.delete()
        await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")

@client.command(name="clear")
async def clear(ctx, amount: int =None):
    if ctx.author.guild_permissions.administrator:
        if amount is None:
            await ctx.send("Please specify the amount of messages to delete in this command.")
        else:
            await ctx.channel.purge(limit=amount+1)
    else:
        await ctx.send("Hey! Sorry but you don't have perms for that command. Duh-Doy!")
@client.command(name="ghostping")
async def ghostping(ctx, *, text):
    if ctx.author.guild_permissions.administrator:
        message = ctx.message
        await message.delete()

@client.command(name="lockdown")
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " is now in lockdown.")

@client.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " has been unlocked.")




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
