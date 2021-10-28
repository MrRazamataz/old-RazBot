import asyncio
import datetime as dt
import enum
import random
import re
import typing as t
from enum import Enum

from discord_slash.utils.manage_commands import create_option, create_choice

from spotifyToYoutube import *
import aiohttp
import discord
import wavelink
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
import aiofiles
vccount = 0
URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class VolumeTooLow(commands.CommandError):
    pass


class VolumeTooHigh(commands.CommandError):
    pass


class MaxVolume(commands.CommandError):
    pass


class MinVolume(commands.CommandError):
    pass


class NoLyricsFound(commands.CommandError):
    pass


class InvalidEQPreset(commands.CommandError):
    pass


class NonExistentEQBand(commands.CommandError):
    pass


class EQGainOutOfBounds(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()

        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"[+] Added `{tracks[0].title}` to the queue.")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.send(f"[+] Added `{track.title}` to the queue.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global vccount
        if not member.bot:
            pass
        else:
            if not before.channel and after.channel:
                vccount = vccount + 1
            elif before.channel and not after.channel:
                vccount = vccount - 1
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "IP address",
                "port": 2333,
                "rest_uri": "http://IP address:2333",
                "password": "password",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    def get_player_slash(self, obj):
        if isinstance(obj, SlashContext):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)
    @commands.command(name="connect", aliases=["join"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}.")

    @cog_ext.cog_slash(name="connect", description="Connect RazBot to the voice channel.",options=[
               create_option(
                 name="channel",
                 description="Select vc if not in one",
                 option_type=7,
                 required=False,
               )
             ])
    async def connect_command_slash(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player_slash(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}.")
    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")
    @connect_command_slash.error
    async def connect_command_error_slash(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")
    @commands.command(name="disconnect", aliases=["leave", "die"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnected.")
    @cog_ext.cog_slash(name="disconnect", description="Remove RazBot from the voice channel")
    async def disconnect_command_slash(self, ctx):
        player = self.get_player_slash(ctx)
        await player.teardown()
        await ctx.send("Disconnected.")
    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)
            channel = ctx.author.voice.channel
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Playback resumed.")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"
            if "open.spotify.com" in query:
                try:
                    embed = discord.Embed(title="__Importent Infomation:__ ", color=0xff0808)
                    embed.set_author(name="RazBot", url="https://razbot.xyz",
                                     icon_url="https://mrrazamataz.ga/archive/RazBot.png")
                    embed.add_field(name="This system is in **beta**, which means it will be buggy and slow.",
                                    value="\u200b", inline=False)
                    embed.add_field(
                        name="THERE IS CURRENTLY A ANTI-RATE LIMIT IN PLACE, SO YOUR SPOTIFY PLAYLISTS WILL ADD SONGS ONE AT A TIME! This is being worked on, but its to prevent being blocked by YouTube.",
                        value="\u200b", inline=True)
                    embed.add_field(
                        name="Issues are things such as getting rate limited by google, \nand the spammy text upon adding to a queue. \nSome of these issues have fixes in the works. ",
                        value="\u200b", inline=True)
                    embed.add_field(name="Please report issues to `MrRazamataz#6614`!", value="\u200b", inline=True)
                    embed.set_footer(text="razbot.xyz")
                    await ctx.send(embed=embed)
                except Exception as e:
                    print(e)
                playlist_id = f"{query[-10:]}.txt"
                directory = 'playlists'
                filenames = os.listdir(directory)
                #full_filepaths = [os.path.join(directory, f) for f in filenames]
                #only_files = [f for f in full_filepaths if os.path.isfile(f)]
                print(filenames)
                print(playlist_id)
                if playlist_id in filenames:
                    await ctx.send("Found playlist in cache!")
                    file = open(f"playlists/{playlist_id}")
                    content = file.read()
                    content_list = content.splitlines()
                    file.close()
                    for line in content_list:
                        print(line)
                        await player.add_tracks(ctx, await self.wavelink.get_tracks(line))
                        length = divmod(player.queue.current_track.length, 60000)
                        await asyncio.sleep(int(length[0]*60))
                    return
                else:
                    await ctx.send("Not found playlist in cache, contacting API...")
                    await ctx.send("Reading your spotify playlist, may take a few moments...")
                    try:
                        # asyncio.run(spotyplaylist(message))
                        query = (spotyplaylist(query))
                        #print(query)
                        await ctx.send("Added to queue, now playing!")
                        save = []
                        for i in query:
                            print(i)
                            f = open(f"playlists/{playlist_id}", "a")
                            f.write(f"{i}\n")
                            f.close()
                            '''
                            #with aiofiles.open(os.path.join(directory, f"{query[-10:]}.txt"), "a") as file:
                            with aiofiles.open (os.path.join(directory, f"test.txt"), "a") as file:
                                print("It ran.")
                                #print(os.path.join(directory, f"test.txt"))

                                await file.write(f"test")
                            '''
                            length = divmod(player.queue.current_track.length, 60000)
                            await asyncio.sleep(int(length[0] * 60))
                        return
                    except Exception as e:
                        print(e)
                        await ctx.send("Try sending the URL without the stuff after `&`.")
            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("[!] No songs to play as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("[!] No suitable voice channel was provided.")

    @cog_ext.cog_slash(name="play", description="Play a song/playlist from YouTube or Spotify")
    async def play_command_slash(self, ctx, *, query: t.Optional[str]):
        player = self.get_player_slash(ctx)

        if not player.is_connected:
            await player.connect(ctx)
            channel = ctx.author.voice.channel
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Playback resumed.")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"
            if "open.spotify.com" in query:
                try:
                    embed = discord.Embed(title="__Importent Infomation:__ ", color=0xff0808)
                    embed.set_author(name="RazBot", url="https://razbot.xyz",
                                     icon_url="https://mrrazamataz.ga/archive/RazBot.png")
                    embed.add_field(name="This system is in **beta**, which means it will be buggy and slow.",
                                    value="\u200b", inline=False)
                    embed.add_field(
                        name="THERE IS CURRENTLY A ANTI-RATE LIMIT IN PLACE, SO YOUR SPOTIFY PLAYLISTS WILL ADD SONGS ONE AT A TIME! This is being worked on, but its to prevent being blocked by YouTube.",
                        value="\u200b", inline=True)
                    embed.add_field(
                        name="Issues are things such as getting rate limited by google, \nand the spammy text upon adding to a queue. \nSome of these issues have fixes in the works. ",
                        value="\u200b", inline=True)
                    embed.add_field(name="Please report issues to `MrRazamataz#6614`!", value="\u200b", inline=True)
                    embed.set_footer(text="razbot.xyz")
                    await ctx.send(embed=embed)
                except Exception as e:
                    print(e)
                playlist_id = f"{query[-10:]}.txt"
                directory = 'playlists'
                filenames = os.listdir(directory)
                #full_filepaths = [os.path.join(directory, f) for f in filenames]
                #only_files = [f for f in full_filepaths if os.path.isfile(f)]
                print(filenames)
                print(playlist_id)
                if playlist_id in filenames:
                    await ctx.send("Found playlist in cache!")
                    file = open(f"playlists/{playlist_id}")
                    content = file.read()
                    content_list = content.splitlines()
                    file.close()
                    for line in content_list:
                        print(line)
                        await player.add_tracks(ctx, await self.wavelink.get_tracks(line))
                        length = divmod(player.queue.current_track.length, 60000)
                        await asyncio.sleep(int(length[0]*60))
                    return
                else:
                    await ctx.send("Not found playlist in cache, contacting API...")
                    await ctx.send("Reading your spotify playlist, may take a few moments...")
                    try:
                        # asyncio.run(spotyplaylist(message))
                        query = (spotyplaylist(query))
                        #print(query)
                        await ctx.send("Added to queue, now playing!")
                        save = []
                        for i in query:
                            print(i)
                            f = open(f"playlists/{playlist_id}", "a")
                            f.write(f"{i}\n")
                            f.close()
                            '''
                            #with aiofiles.open(os.path.join(directory, f"{query[-10:]}.txt"), "a") as file:
                            with aiofiles.open (os.path.join(directory, f"test.txt"), "a") as file:
                                print("It ran.")
                                #print(os.path.join(directory, f"test.txt"))

                                await file.write(f"test")
                            '''
                            length = divmod(player.queue.current_track.length, 60000)
                            await asyncio.sleep(int(length[0] * 60))
                        return
                    except Exception as e:
                        print(e)
                        await ctx.send("Try sending the URL without the stuff after `&`.")
            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))
    @play_command_slash.error
    async def play_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("[!] No songs to play as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("[!] No suitable voice channel was provided.")
    @commands.command(name="pause")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send("Playback paused. ⏸️")

    @cog_ext.cog_slash(name="pause", description="Pause the currently playing song")
    async def pause_command_slash(self, ctx):
        player = self.get_player_slash(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send("Playback paused. ⏸️")
    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("[!] Already paused.")
    @pause_command_slash.error
    async def pause_command_error_slash(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("[!] Already paused.")
    @commands.command(name="stop")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped. 🛑")

    @cog_ext.cog_slash(name="stop", description="Stop the current song and clear the queue")
    async def stop_command_slash(self, ctx):
        player = self.get_player_slash(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped. 🛑")
    @commands.command(name="next", aliases=["skip", "n" ,"s"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send("[/] Playing next track in queue.")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @cog_ext.cog_slash(name="skip", description="Skip to the next song in queue")
    async def next_command_slash(self, ctx):
        player = self.get_player_slash(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send("[/] Playing next track in queue.")
    @next_command_slash.error
    async def next_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")
    @commands.command(name="previous", aliases=["back"])
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send("Playing previous track in queue.")
    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")

    @cog_ext.cog_slash(name="back", description="Go back a track in queue")
    async def previous_command_slash(self, ctx):
        player = self.get_player_slash(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send("Playing previous track in queue.")
    @previous_command_slash.error
    async def previous_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")
    @commands.command(name="shuffle")
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue could not be shuffled as it is currently empty. :0")

    @cog_ext.cog_slash(name="shuffle", description="Shuffle the queue")
    async def shuffle_command_slash(self, ctx):
        player = self.get_player_slash(ctx)
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")
    @shuffle_command_slash.error
    async def shuffle_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue could not be shuffled as it is currently empty. :0")
    @commands.command(name="repeat",aliases=["loop"])
    async def repeat_command(self, ctx, mode: str):
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.send(f"The repeat mode has been set to {mode}.")

    @cog_ext.cog_slash(name="loop", description="Select a loop mode", options=[
               create_option(
                 name="loop",
                 description="Loop mode options",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="all",
                    value="all"
                  ),
                  create_choice(
                    name="1",
                    value="1"
                  ),
                create_choice(
                    name="none",
                    value="none"
                )
                ]
               )
             ])
    async def repeat_command_slash(self, ctx, loop: str):
        if loop not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player_slash(ctx)
        player.queue.set_repeat_mode(loop)
        await ctx.send(f"The repeat mode has been set to {loop}.")
    @commands.command(name="queue", aliases=["q"])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="RazBot Music System:")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing. :0"),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        msg = await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")

    @cog_ext.cog_slash(name="queue", description="Show the queue with a default length of 10", options=[
               create_option(
                 name="length",
                 description="Select the queue show length (default 10).",
                 option_type=4,
                 required=False,
                 choices=[
                  create_choice(
                    name="length",
                    value=10
                  )
                ]
               )
             ])
    async def queue_command_slash(self, ctx, length: int):
        player = self.get_player_slash(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {length} tracks",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="RazBot Music System:")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing. :0"),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:length]),
                inline=False
            )

        msg = await ctx.send(embed=embed)
    @queue_command.error
    async def queue_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")
    # Requests -----------------------------------------------------------------

    @commands.group(name="volume", invoke_without_command=True, aliases=["vol", "v"])
    async def volume_group(self, ctx, volume: int):
        player = self.get_player(ctx)

        if volume < 0:
            raise VolumeTooLow

        if volume > 150:
            raise VolumeTooHigh

        await player.set_volume(volume)
        await ctx.send(f"Volume set to {volume:,}%")

    @cog_ext.cog_slash(name="volume", description="Change the volume between 1%-150%")
    async def volume_group_slash(self, ctx, volume: int):
        player = self.get_player_slash(ctx)

        if volume < 0:
            raise VolumeTooLow

        if volume > 150:
            raise VolumeTooHigh

        await player.set_volume(volume)
        await ctx.send(f"Volume set to {volume:,}%")
    @volume_group.error
    async def volume_group_error(self, ctx, exc):
        if isinstance(exc, VolumeTooLow):
            await ctx.send("The volume must be 0% or above.")
        elif isinstance(exc, VolumeTooHigh):
            await ctx.send("The volume must be 150% or below.")

    @volume_group.command(name="up")
    async def volume_up_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 150:
            raise MaxVolume

        await player.set_volume(value := min(player.volume + 10, 150))
        await ctx.send(f"Volume set to {value:,}%")

    @volume_up_command.error
    async def volume_up_command_error(self, ctx, exc):
        if isinstance(exc, MaxVolume):
            await ctx.send("The player is already at max volume.")

    @volume_group.command(name="down")
    async def volume_down_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume

        await player.set_volume(value := max(0, player.volume - 10))
        await ctx.send(f"Volume set to {value:,}%")

    @volume_down_command.error
    async def volume_down_command_error(self, ctx, exc):
        if isinstance(exc, MinVolume):
            await ctx.send("The player is already at min volume.")

    @commands.command(name="lyrics")
    async def lyrics_command(self, ctx, name: t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyricsFound

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    await ctx.send("Lyrics too long for discord")
                    return await ctx.send(f"<{data['links']['genius']}>")

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=ctx.author.colour,
                    timestamp=dt.datetime.utcnow(),
                )
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.send(embed=embed)

    @lyrics_command.error
    async def lyrics_command_error(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            await ctx.send("[!] No lyrics could be found. 😦")

    @cog_ext.cog_slash(name="lyrics", description="Attempt to find the lyrics to the playing song")
    async def lyrics_command_slash(self, ctx):
        player = self.get_player_slash(ctx)
        name = player.queue.current_track.title

        async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
            if not 200 <= r.status <= 299:
                raise NoLyricsFound

            data = await r.json()

            if len(data["lyrics"]) > 2000:
                await ctx.send("Lyrics too long for discord")
                return await ctx.send(f"<{data['links']['genius']}>")

            embed = discord.Embed(
                title=data["title"],
                description=data["lyrics"],
                colour=ctx.author.colour,
                timestamp=dt.datetime.utcnow(),
            )
            embed.set_thumbnail(url=data["thumbnail"]["genius"])
            embed.set_author(name=data["author"])
            await ctx.send(embed=embed)
    @lyrics_command_slash.error
    async def lyrics_command_error_slash(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            await ctx.send("[!] No lyrics could be found. 😦")

    @commands.command(name="eq")
    async def eq_command(self, ctx, preset: str):
        player = self.get_player(ctx)

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            raise InvalidEQPreset

        await player.set_eq(eq())
        await ctx.send(f"Equaliser adjusted to the {preset} preset.")

    @eq_command.error
    async def eq_command_error(self, ctx, exc):
        if isinstance(exc, InvalidEQPreset):
            await ctx.send("The EQ preset must be either 'flat', 'boost', 'metal', or 'piano'.")

    @commands.command(name="adveq", aliases=["aeq"])
    async def adveq_command(self, ctx, band: int, gain: float):
        player = self.get_player(ctx)

        if not 1 <= band <= 15 and band not in HZ_BANDS:
            raise NonExistentEQBand

        if band > 15:
            band = HZ_BANDS.index(band) + 1

        if abs(gain) > 10:
            raise EQGainOutOfBounds

        player.eq_levels[band - 1] = gain / 10
        eq = wavelink.eqs.Equalizer(levels=[(i, gain) for i, gain in enumerate(player.eq_levels)])
        await player.set_eq(eq)
        await ctx.send("Equaliser adjusted.")

    @adveq_command.error
    async def adveq_command_error(self, ctx, exc):
        if isinstance(exc, NonExistentEQBand):
            await ctx.send(
                "This is a 15 band equaliser -- the band number should be between 1 and 15, or one of the following "
                "frequencies: " + ", ".join(str(b) for b in HZ_BANDS)
            )
        elif isinstance(exc, EQGainOutOfBounds):
            await ctx.send("The EQ gain for any band should be between 10 dB and -10 dB.")

    @commands.command(name="playing", aliases=["np"])
    async def playing_command(self, ctx):
        player = self.get_player(ctx)

        if not player.is_playing:
            raise PlayerIsAlreadyPaused

        embed = discord.Embed(
            title="Now playing:",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_author(name="Playback Information:")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Track title", value=player.queue.current_track.title, inline=False)
        embed.add_field(name="Artist", value=player.queue.current_track.author, inline=False)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)
        embed.add_field(
            name="Position:",
            value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}",
            inline=False
        )

        await ctx.send(embed=embed)

    @playing_command.error
    async def playing_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("There is no track currently playing.")

    @cog_ext.cog_slash(name="np", description="Show info on the currently playing song")
    async def playing_command_slash(self, ctx):
        player = self.get_player_slash(ctx)

        if not player.is_playing:
            raise PlayerIsAlreadyPaused

        embed = discord.Embed(
            title="Now playing:",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_author(name="Playback Information:")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Track title", value=player.queue.current_track.title, inline=False)
        embed.add_field(name="Artist", value=player.queue.current_track.author, inline=False)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)
        embed.add_field(
            name="Position:",
            value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}",
            inline=False
        )

        await ctx.send(embed=embed)
    @playing_command_slash.error
    async def playing_command_error_slash(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("There is no track currently playing.")
    @commands.command(name="skipto", aliases=["playindex", "jumpto"])
    async def skipto_command(self, ctx, index: int):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks

        player.queue.position = index - 2
        await player.stop()
        await ctx.send(f"Playing track in position {index}.")

    @skipto_command.error
    async def skipto_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("That index is out of the bounds of the queue.")

    @cog_ext.cog_slash(name="jumpto", description="Jump to a specific song in the queue")
    async def skipto_command_slash(self, ctx, index: int):
        player = self.get_player_slash(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks

        player.queue.position = index - 2
        await player.stop()
        await ctx.send(f"Playing track in position {index}.")
    @skipto_command_slash.error
    async def skipto_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("That index is out of the bounds of the queue.")
    @commands.command(name="restart", aliases=["replay"])
    async def restart_command(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        await ctx.send("Track restarted.")

    @cog_ext.cog_slash(name="replay", description="Replay the current song")
    async def restart_command_slash(self, ctx):
        player = self.get_player_slash(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        await ctx.send("Track restarted.")

    @restart_command.error
    async def restart_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
    @restart_command_slash.error
    async def restart_command_error_slash(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")

    @commands.command(name="seek", aliases=["jump"])
    async def seek_command(self, ctx, position: str):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.send(f"I have jumped to `{position}` in the playing song.")

    @cog_ext.cog_slash(name="jump", description="Jump to a timestamp position in the current song")
    async def seek_command_slash(self, ctx, position: str):
        player = self.get_player_slash(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.send(f"I have jumped to `{position}` in the playing song.")
    @commands.command(name="vccount")
    async def vccount_command(self, ctx):
        global vccount
        await ctx.send(f"There are currently `{vccount}` connected voice channel(s)!")
    @commands.command(name="resetvccount")
    async def resetvccount_command(self, ctx):
        global vccount
        vccount = 0
        await ctx.send(f"There are currently `{vccount}` connected voice channel(s)!")
    @cog_ext.cog_slash(name="vccount", description="Show how many VC channels RazBot is in globally")
    async def vccount_command_slash(self, ctx):
        global vccount
        await ctx.send(f"There are currently `{vccount}` connected voice channel(s)!")
def setup(bot):
    bot.add_cog(Music(bot))