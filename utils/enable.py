import logging
logger = logging.getLogger(__name__)

import json
from discord.commands import Option
import discord
import utils.command as command

def wtire(file, value: str):
    f = open(file, mode='a', encoding='utf-8', newline='\n')
    logger.info(f'{file}を読み込みました')
    f.write(value)
    logger.info(f'{value}を書き込みました')
    f.close

def remove(file, value: str, next: str):
    with open(file, encoding='utf-8') as f:
        data_lines = f.read()
    logger.info(f'{file}を読み込みました')
    data_lines = data_lines.replace(value, next)
    with open(file, mode='w', encoding='utf-8') as f:
        f.write(data_lines)
    f.close

def read(file):
    with open(file) as temp_f:
        datafile = temp_f.readlines()
    logger.info(f'{file}を読み込みました')
    return datafile

def check(file, data: str) ->bool :
    logger.info(f'{file}を読み込みました')
    datafile = read(file)
    for line in datafile:
        if data in line:
            logger.info(f'{data}がファイル内と一致しました')
            return True
    logger.info(f'{data}はファイル内に含まれていません')
    return False

def setup(bot):
    logger.info('enableが正常に読み込まれました')

