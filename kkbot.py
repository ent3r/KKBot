"""Koden til boten i KodeKafe discord serveren"""
# pylint: disable=broad-except


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


DESCRIPTION = "The bot in use in the KodeKafe discord server"
PREFIX = ">"


async def handle_error(ctx, error, readable_error=None):
    """Handles errors in commands"""
    embed = discord.Embed(
        title="Error",
        description="An error occured",
        colour=discord.Color.red(),
        author="KKBot",
    )
    if readable_error:
        embed.add_field(name="Error message",
                        value=readable_error, inline=True)
    else:
        embed.add_field(name="Error message", value=error, inline=True)
    await ctx.send(embed=embed)
    print(f"Readable error: {readable_error}")
    raise error


class Bot(commands.Bot):
    """The framework for our bot"""

    def __init__(self):
        super().__init__(command_prefix=PREFIX, description=DESCRIPTION)

    async def on_ready(self):
        """Ready function"""
        print('------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        activity = discord.activity.Activity(
            name="for commands", type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx, error):  # pylint: disable=arguments-differ
        """Handles errors by sending a message in the channel"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Error: Command not found")
            raise error
        raise error


class Utilities(commands.Cog):
    """Utility commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Command for checking the bot's response time"""
        await ctx.send(f'Response time: {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def botname(self, ctx):
        """Tells you the BOT's name."""
        await ctx.send(BOT.user.name)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.name} joined in {member.joined_at}')

    @commands.command()
    async def status(self, ctx):
        """Checks bot status, including uptime"""

        for item in RESPONSE:
            if item["type"] == 2:
                data = item
                break

        content = discord.Embed(
            title="KKBot status",
            description="""
            Status on the bot, incuding uptime, last downtime, and last command status""",
            colour=discord.Color.red(),
            author="KKBot",
        )

        content.add_field(name="Uptime", value=(
            str(datetime.timedelta(seconds=(int(time.time()) - data["datetime"])))), inline=True)

        content.add_field(name="Last downtime", value=datetime.datetime.fromtimestamp(
            data["datetime"]), inline=True)
        await ctx.send(embed=content)


class Math(commands.Cog):
    """Cog for math commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *numbers):
        """Adds two numbers together."""
        numbers_int = []
        try:
            for number in numbers:
                numbers_int.append(int(number))
        except Exception as err:
            handle_error(ctx, err, "Cannot convert char to int")
            return
        await ctx.send(sum(numbers_int))
        print("Add command succeed")

    @commands.command()
    async def sqrt(self, ctx, number):
        """Finds the square root of any number"""
        try:
            number = int(number)
        except Exception as err:
            handle_error(ctx, err, "Cannot convert char to int")
        square = mathfunc.sqrt(number)
        await ctx.send(f"The square root of {number} is {square}\n┏┓\n┗┛")


class Fun(commands.Cog):
    """Cog for fun and game commands"""

    def __init__(self, bot):
        self.bot = bot

    async def groot(self, ctx):
        """I am Groot"""
        await ctx.send("I am Groot")

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def randomcommand(self, ctx):
        """Just try it."""
        await ctx.send("Why are you typing bullshit?")

    @commands.command()
    async def cool(self, ctx):
        """Says if a user is cool."""
        if ctx.invoked_subcommand is None:
            if random.randint(0, 1) == 0:
                await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))
                return
            else:
                await ctx.send('Yes, {0.subcommand_passed} is cool :)'.format(ctx))
                return


BOT = Bot()
BOT.add_cog(Utilities(BOT))
BOT.add_cog(Math(BOT))
BOT.add_cog(Fun(BOT))



TOKEN = os.getenv("KKBOTTOKEN")
if TOKEN is None:
    raise EnvironmentError("Missing token")

try:
    print("Starting...")
    BOT.run(TOKEN)
    print("Closed")
except KeyboardInterrupt:
    print("Forceibly closing connection...", end="")
    BOT.close()
    print("Connection closed")
