import logging
from unittest import removeResult

import yaml.loader
logger = logging.getLogger(__name__)

import json
import yaml
from discord.commands import Option
import discord
import utils.command as command # guild_ids=command.server_id

from dictknife import deepmerge
from pydantic import FilePath

def wtire(file: FilePath, value: str):
    logger.info(f'{file}を読み込みました')
    f = open(file, mode='a', encoding='utf-8', newline='\n')
    f.write(value)
    f.close

def remove(file: FilePath, value: str, next: str):
    logger.info(f'{file}を読み込みました')
    with open(file, encoding='utf-8') as f:
        data_lines = f.read()
    data_lines = data_lines.replace(value, next)
    with open(file, mode='w', encoding='utf-8') as f:
        f.write(data_lines)
    f.close

def read(file: FilePath) -> str:
    logger.info(f'{file}を読み込みました')
    with open(file) as temp_f:
        datafile = temp_f.readlines()
    
    return datafile

def check(file: FilePath, data: str) -> bool:
    logger.info(f'{file}を読み込みました')
    datafile = read(file)
    for line in datafile:
        if data in line:
            logger.info(f'{data}がファイル内と一致しました')
            return True
    logger.info(f'{data}はファイル内に含まれていません')
    return False

def write_yaml(file: FilePath, flash: list):
    logger.info(flash)
    try:
        with open(file, 'r') as yml:
            data = yaml.safe_load(yml)
        logger.info(data)
    except Exception as e:
        logger.error(e)
        logger.info('既存ファイルの読み込みをスキップしました')
    with open(file, 'w')as f:
        try:
            yaml.dump(deepmerge(data, flash), f, default_flow_style=False, allow_unicode=True)
            logger.info('2つ書き込み')
        except Exception as e:
            yaml.dump(flash, f, default_flow_style=False, allow_unicode=True)
            logger.error(e)
            logger.info('1つ書き込み')

def read_yaml(file: FilePath) -> dict:
    try:
        with open(file, 'r') as yml:
            data = yaml.safe_load(yml)
    except Exception as e:
        logger.error(e)
        return None
    return data

def setup(bot):
    logger.info('enableが正常に読み込まれました')

