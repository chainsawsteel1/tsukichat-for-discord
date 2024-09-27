import logging
logger = logging.getLogger(__name__)

import discord
import re
import utils.romaji as romaji
import utils.command as command
import utils.enable as enable

romaji.Converter.init_map('./txt/hiragana.txt')

def check_ng_word(target_text: str) -> bool:
    try:
        with open('./txt/ngwords.txt', 'r', encoding='utf-8') as file:
            ng_words = [line.strip() for line in file.readlines()]
            for ng_word in ng_words:
                if ng_word in target_text:
                    return True
            return False
    except Exception as e:
        logger.exception(e)
        return False

def is_romaji_only(text: str) -> bool:
    return re.match(r'^[!-~\\s]+$', text) and re.search(r'[a-z]', text)

def setup(bot: discord.Bot):
    logger.info('replyが正常に読み込まれました')

    async def send_webhook(message: discord.Message, msg: str):
        webhook = discord.utils.get(await message.channel.webhooks(), name='tsukihook')
        if not webhook:
            webhook = await message.channel.create_webhook(name='tsukihook')
        await webhook.send(
            content=msg,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
        )

    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        elif not message.content:
            return
        
        elif check_ng_word(message.content):
            logger.warning(f'メッセージ「{message.content}」はngwordを含んでいます')
            return
        
        if is_romaji_only(message.content):
            try:
                if enable.check('./txt/noconv.txt', message.content) == False:
                    conf = enable.read_yaml(f'./users/{message.author.mention}.yml')
                    logger.info(conf)
                    if conf == None:
                        conf = {f'convert_mode': f'{True}'}
                    conv_msg = romaji.Converter.romaji_to_japanese(message.content)
                    send = f'-# {message.content}\n{conv_msg}'
                    logger.info(f'変換しました「{send}」')
                    if conf['convert_mode'] == 'True':
                        try:
                            await send_webhook(message, send)
                            logger.info('webhookで送信しました')
                        except:
                            await message.reply(f'{conv_msg}\n-# 問題が発生しました', mention_author=False)
                            logger.warning('問題が発生したためreplyで送信しました')
                    else:
                        try:
                            await message.reply(conv_msg, mention_author=False)
                            logger.info('replyで送信しました')
                        except Exception as e:
                            logger.error(e)
                            await send_webhook(message, send + f'\n-# 問題が発生しました\n```{e}```')
                            logger.warning('問題が発生したためwebhookで送信しました')
            except Exception as e:
                await message.channel.send(f'問題が発生しました\n```{e}```')
                logger.exception(e)
                raise
