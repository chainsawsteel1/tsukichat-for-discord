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


    @bot.slash_command(description='変換時の返信モードを変更します')
    async def mode(
        ctx: discord.ApplicationContext,
        status: Option(str, 'モード', choices=['webhook', '返信']) # type: ignore
        ):
        try:
            if status == 'webhook':
                status = True
            else:
                status = False
            data = {
                f'convert_mode': f'{status}'
            }
            enable.write_yaml(f'./users/{ctx.author.mention}.yml', data)
            logger.info(f'{ctx.author.mention}の設定を{status}にへんこうしました')
            await ctx.respond('設定を変更しました')
        except Exception as e:
            await ctx.respond(f'問題が発生しました\n```{e}```')
            logger.exception(e)