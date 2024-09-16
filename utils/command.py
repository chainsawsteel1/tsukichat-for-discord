import logging
logger = logging.getLogger(__name__)

import discord
import utils.enable as enable
import utils.reply as reply
import asyncio
from discord.commands import Option

def setup(bot):
    logger.info('commandが正常に読み込まれました')

    @bot.slash_command(description='生存確認')
    async def ping(ctx: discord.ApplicationContext):
        await ctx.respond('pong!')
        logger.info(f'pingコマンドが{ctx.author.mention}によって利用されました')