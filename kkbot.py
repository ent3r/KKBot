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


# region api stuff
API_URL = "https://api.uptimerobot.com/v2/getMonitors"
PAYLOAD = "api_key=m783949605-da40969d1f5b232744446ac8&format=json&logs=1"
HEADERS = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
}
RESPONSE = json.loads(requests.request(
    "POST", API_URL, data=PAYLOAD, headers=HEADERS).text)["monitors"][0]["logs"]
# endregion
# region bot info
DESCRIPTION = "The bot in use in the KodeKafe discord server"
PREFIX = "!"
# endregion

BOT = commands.Bot(command_prefix=PREFIX, description=DESCRIPTION)


async def handle_error(ctx, error, readable_error=None):
    """Handles errors in commands"""
    embed = discord.Embed(
        title="Error",
        description="An error occured",
        colour=discord.Color.red(),
        author="KKBot",
    )
    if readable_error is not None:
        embed.add_field(name="Error message",
                        value=readable_error, inline=True)
    else:
        embed.add_field(name="Error message", value=error, inline=True)
    await ctx.send(embed=embed)
    raise error


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


@BOT.event
async def on_command_error(ctx, error):
    """Handles errors by sending a message in the channel"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Error: Command not found")
        raise error
    raise error


# region math commands

@BOT.group()
async def math(ctx):
    """Wrapper for math functions"""
    if ctx.invoked_subcommand is None:
        await ctx.send("Error: No subcommand passed")


@math.command()
async def add(ctx, *numbers):
    """Adds two numbers together."""
    numbers_int = []
    try:
        for number in numbers:
            numbers_int.append(int(number))
    except ValueError:
        await ctx.send("Error: Cannot convert letters to int")
        print("Add command failed")
        return
    await ctx.send(sum(numbers_int))
    print("Add command succeed")


@math.command()
async def sqrt(ctx, number):
    """Finds the square root of any number"""
    try:
        number = int(number)
    except ValueError:
        await ctx.send("Error: Cannot convert letter to int")
        return
    square = mathfunc.sqrt(number)
    await ctx.send(f"The square root of {number} is {square}\n┏┓\n┗┛")

# endregion


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
    await ctx.send(embed=content)


@BOT.command()
async def ping(ctx):
    """Command for checking the bot's response time"""
    await ctx.send(f'Response time: {round(BOT.latency * 1000)}ms')


@BOT.command()
async def randomcommand(ctx):
    """Just try it."""
    await ctx.send("Why are you typing bullshit?")


@BOT.command()
async def groot(ctx):
    """I am Groot"""
    await ctx.send("I am Groot")


@BOT.command()
async def botname(ctx):
    """Tells you the BOT's name."""
    await ctx.send(BOT.user.name)


@BOT.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except ValueError:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@BOT.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@BOT.command()
async def repeat(ctx, times: int, *content):
    """Repeats a message multiple times."""
    for _ in range(times):
        await ctx.send(content)
        time.sleep(0.2)


@BOT.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@BOT.group()
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None:
        if random.randint(0, 1) == 0:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))
            return
        else:
            await ctx.send('Yes, {0.subcommand_passed} is cool :)'.format(ctx))
            return

TOKEN = os.getenv("KKBOTTOKEN")
if TOKEN is None:
    raise EnvironmentError("Missing token")


try:
    print("Starting bot...")
    BOT.run(TOKEN)
    print("Closed")
except KeyboardInterrupt:
    print("Forceibly closing connection...", end="")
    BOT.close()
    print("Connection closed")
