import asyncio

import constants
import taskbot
from commandbot import command_bot

import discord

task_bot = taskbot.Bot(intents=discord.Intents.all(), activity=discord.Game(name='DNX | !help'))

event_loop = asyncio.get_event_loop()
event_loop.create_task(task_bot.start(constants.DISCORD_TOKEN))
event_loop.create_task(command_bot.start(constants.DISCORD_TOKEN))

try:
    event_loop.run_forever()
except KeyboardInterrupt:
    event_loop.stop()
    event_loop.close()
