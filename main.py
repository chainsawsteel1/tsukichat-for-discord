import logging
import logging.handlers
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            "discord.log",
            encoding="utf-8",
            backupCount=5,
        ),
    ],
    encoding="utf-8",
)
logger = logging.getLogger(__name__)

import discord
from discord.ext import tasks
import random
import os
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot(
    intents=discord.Intents.all(),
    activity=discord.Game('Starting up...'),
)

import utils.command as command
command.setup(bot)

import utils.enable as enable
enable.setup(bot)

import utils.reply as reply
reply.setup(bot)

@tasks.loop(seconds=10)
async def update_status():
    guild_count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=f'Servers: {guild_count}'))

@bot.event
async def on_ready():
    logger.info('botが起動しました')
    update_status.start()

bot.run(os.environ["BOT_TOKEN"])