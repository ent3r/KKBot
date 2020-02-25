"""Koden til boten i KodeKafe discord serveren"""

import datetime
import json
import math as mathfunc
import os
import random
import time

import requests

import discord
from discord.ext import commands

API_URL = "https://api.uptimerobot.com/v2/getMonitors"
PAYLOAD = "api_key=m783949605-da40969d1f5b232744446ac8&format=json&logs=1"
HEADERS = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
}

RESPONSE = json.loads(requests.request(
    "POST", API_URL, data=PAYLOAD, headers=HEADERS).text)["monitors"][0]["logs"]


DESCRIPTION = '''A general bot with general commands'''
BOT = commands.Bot(command_prefix='?', description=DESCRIPTION)
LAST_COMMAND = {"exit code": None, "command": None, "params": None}


@BOT.event
async def on_ready():
    """Ready function"""
    print('------')
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    print('------')
    activity = discord.activity.Activity(
        name="for commands", type=discord.ActivityType.watching)
    await BOT.change_presence(activity=activity)

# @BOT.category()
# class math()*


@BOT.group()
async def math(ctx):
    """Wrapper for math functions"""
    if ctx.invoked_subcommand is None:
        await ctx.send("Error: No subcommand passed")


@math.command()
async def add(ctx, *numbers):
    """Adds two numbers together."""
    LAST_COMMAND["command"] = "add"
    LAST_COMMAND["args"] = numbers
    numbers_int = []
    try:
        for number in numbers:
            numbers_int.append(int(number))
    except ValueError:
        await ctx.send("Error: Cannot convert letters to int")
        print("Add command failed")
        LAST_COMMAND["exit code"] = 1
        return
    await ctx.send(sum(numbers_int))
    print("Add command succeed")


@math.command()
async def sqrt(ctx, number):
    """Finds the square root of any number"""
    LAST_COMMAND["command"] = "square"
    LAST_COMMAND["params"] = None
    try:
        number = int(number)
    except ValueError:
        await ctx.send("Error: Cannot convert letter to int")
        LAST_COMMAND["exit code"] = 1
        return
    square = mathfunc.sqrt(number)
    await ctx.send(f"The square root of {number} is {square}\n┏┓\n┗┛")
    LAST_COMMAND["exit code"] = 0


@BOT.command()
async def status(ctx):
    """Checks BOT status, including uptime"""

    for item in RESPONSE:
        if item["type"] == 2:
            data = item
            break

    content = discord.Embed(
        title="KKBot status",
        description="Status on the bot, incuding uptime, last downtime, and last command status",
        colour=discord.Color.red(),
        author="KKBot",
    )

    content.add_field(name="Uptime", value=(
        str(datetime.timedelta(seconds=(int(time.time()) - data["datetime"])))), inline=True)

    content.add_field(name="Last downtime", value=datetime.datetime.fromtimestamp(
        data["datetime"]), inline=True)
    content.add_field(name="Last Command",
                      value=LAST_COMMAND["command"], inline=False)
    content.add_field(name="Exit code", value=str(
        LAST_COMMAND["exit code"]), inline=True)
    content.add_field(name="Parameters",
                      value=LAST_COMMAND["params"], inline=True)
    await ctx.send(embed=content)


@BOT.command()
async def ping(ctx):
    """Command for checking the bot's response time"""
    await ctx.send(f'Response time: {round(BOT.latency * 1000)}ms')


@BOT.command()
async def randomcommand(ctx):
    """Just try it."""
    LAST_COMMAND["command"] = "randomcommand"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send("Why are you typing bullshit?")


@BOT.command()
async def groot(ctx):
    """I am Groot"""
    LAST_COMMAND["command"] = "groot"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send("I am Groot")


@BOT.command()
async def botname(ctx):
    """Tells you the BOT's name."""
    LAST_COMMAND["command"] = "botname"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send(BOT.user.name)


@BOT.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    LAST_COMMAND["command"] = "randomcommand"
    LAST_COMMAND["params"] = dice
    try:
        rolls, limit = map(int, dice.split('d'))
    except ValueError:
        await ctx.send('Format has to be in NdN!')
        LAST_COMMAND["exit code"] = 1
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
    LAST_COMMAND["exit code"] = 0


@BOT.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    LAST_COMMAND["command"] = "choose"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    await ctx.send(random.choice(choices))
    LAST_COMMAND["exit code"] = 0


@BOT.command()
async def repeat(ctx, times: int, *content):
    """Repeats a message multiple times."""
    LAST_COMMAND["command"] = "repeat"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    for _ in range(times):
        await ctx.send(content)
        time.sleep(0.2)
    LAST_COMMAND["exit code"] = 0


@BOT.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    LAST_COMMAND["command"] = "joined"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
    LAST_COMMAND["exit code"] = 0


@BOT.group()
async def cool(ctx):
    """Says if a user is cool."""
    LAST_COMMAND["command"] = "cool"
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    if ctx.invoked_subcommand is None:
        if random.randint(0, 1) == 0:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))
            LAST_COMMAND["exit code"] = 0
            return
        else:
            await ctx.send('Yes, {0.subcommand_passed} is cool :)'.format(ctx))
            LAST_COMMAND["exit code"] = 0
            return
        LAST_COMMAND["exit code"] = 3
    LAST_COMMAND["exit code"] = 4

token = os.getenv("KKBOTTOKEN")
if token == None:
    raise EnvironmentError("Missing discord token")

try:
    print("Starting bot...")
    BOT.run(token)
    print("Closed")
except KeyboardInterrupt:
    print("Forceibly closing connection...", end="")
    BOT.close()
    print("Connection closed")
