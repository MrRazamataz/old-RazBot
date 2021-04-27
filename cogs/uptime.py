# MrRazamataz's RazBot
# uptime command
import random
import discord
from discord import reaction
from discord.ext import commands
import asyncio
import os
import aiofiles
import time

class uptime(commands.Cog):
    def __init__(self, client, time_difference_seconds):
        self.client = client

    @commands.command(name="uptime")
    def seconds_days(self, time_difference_seconds):
        # Finds the number of mins
        time_difference_minutes = time_difference_seconds // 60
        # Finds the excess number of seconds
        seconds = (time_difference_seconds - (time_difference_minutes * 60))
        # Finds the number of hours
        time_difference_hours = time_difference_minutes // 60
        # Finds the excess number of mins
        mins = (time_difference_minutes - (time_difference_hours * 60))
        # Finds the number of days
        time_difference_days = time_difference_hours // 24
        # Finds the excess number of hours
        hours = (time_difference_hours - (time_difference_days * 24))

        # Finds the excess number of days
        days = time_difference_days

        return seconds, mins, hours, days


def setup(client):
    client.add_cog(uptime(client))
