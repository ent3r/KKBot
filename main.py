"""Koden til boten i KodeKafe discord serveren"""

from threading import Thread
import os
import random
import time
import json
import datetime
import requests
import discord
from discord.ext import commands
from flask import Flask


API_URL = "https://api.uptimerobot.com/v2/getMonitors"
PAYLOAD = "api_key=m783949605-da40969d1f5b232744446ac8&format=json&logs=1"
HEADERS = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
}

RESPONSE = json.loads(requests.request(
    "POST", API_URL, data=PAYLOAD, headers=HEADERS).text)["monitors"][0]["logs"]


DESCRIPTION = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
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


@BOT.command()
async def add(ctx, left, right):
    """Adds two numbers together."""
    LAST_COMMAND["command"] = "add"
    LAST_COMMAND["params"] = {"left": left, "right": right}
    try:
        left = int(left)
        right = int(right)
    except ValueError:
        await ctx.send("Cannot convert letters to int")
        print("Add command failed")
        LAST_COMMAND["exit code"] = 1
        return
    await ctx.send(left + right)
    print("Add command sucseeded")


@BOT.command()
async def status(ctx):
    """Checks BOT status, including uptime"""

    for item in RESPONSE:
        if item["type"] == 1:
            data = item
            break

    content = discord.Embed(
        title="KKBot status",
        description="Status on the bot, incuding uptime, last downtime, and last command status",
        colour=discord.Color.red()
    )


    content.add_field(name="Uptime", value=(
        (int(time.time()) - data["datetime"])/60)/60, inline=True)


    content.add_field(name="Last downtime", value=datetime.datetime.fromtimestamp(
        data["datetime"]), inline=True)
    content.add_field(name="Last Command", value=LAST_COMMAND["command"], inline=False)
    content.add_field(name="Exit code", value=str(LAST_COMMAND["exit code"]), inline=True)
    content.add_field(name="Parameters", value=LAST_COMMAND["params"], inline=True)
    await ctx.send(embed=content)



@BOT.command()
async def randomcommand(ctx):
    """Just try it."""
    LAST_COMMAND["command"] = randomcommand
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send("Why're you typing bullshit?")


@BOT.command()
async def groot(ctx):
    """I am Groot"""
    LAST_COMMAND["command"] = groot
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send("I am Groot")


@BOT.command()
async def square(ctx):
    """Draws an (inperfect) square."""
    LAST_COMMAND["command"] = square
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send("____")
    await ctx.send("|_|")


@BOT.command()
async def botname(ctx):
    """Tells you the BOT's name."""
    LAST_COMMAND["command"] = botname
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send(BOT.user.name)


@BOT.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    LAST_COMMAND["command"] = randomcommand
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
    LAST_COMMAND["command"] = choose
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    await ctx.send(random.choice(choices))
    LAST_COMMAND["exit code"] = 0


@BOT.command()
async def repeat(ctx, times: int, *content):
    """Repeats a message multiple times."""
    LAST_COMMAND["command"] = botname
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    for _ in range(times):
        await ctx.send(content)
        time.sleep(0.2)
    LAST_COMMAND["exit code"] = 0


@BOT.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    LAST_COMMAND["command"] = botname
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 1
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
    LAST_COMMAND["exit code"] = 0


@BOT.group()
async def cool(ctx):
    """Says if a user is cool."""
    LAST_COMMAND["command"] = botname
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
        LAST_COMMAND["exit code"] = 2
    LAST_COMMAND["exit code"] = 3


@cool.command(name='BOT')
async def _bot(ctx):
    """Is the bot cool?"""
    LAST_COMMAND["command"] = botname
    LAST_COMMAND["params"] = None
    LAST_COMMAND["exit code"] = 0
    await ctx.send('Yes, the bot is cool.')
    LAST_COMMAND["exit code"] = 1

APP = Flask("Server settings")


@APP.route("/")
def index():
    """Function for the index page of the site"""
    return "<h1>Bot is running</h1>"


Thread(target=APP.run, args=("0.0.0.0", 8080)).start()

try:
    BOT.run(os.environ.get("TOKEN"))
except KeyboardInterrupt:
    BOT.close()
