from os import environ

from logging import (INFO, FileHandler, StreamHandler, basicConfig,
                     error, getLogger, info, warning)


LOGGER = getLogger(__name__)

TOKEN_TIMEOUT = environ.get('TOKEN_TIMEOUT', '60')
if TOKEN_TIMEOUT.isdigit():
    TOKEN_TIMEOUT = int(TOKEN_TIMEOUT)
else:
    TOKEN_TIMEOUT = '60'

DM_MODE = environ.get('DM_MODE', True)

user_data = {}
config_dict = {"DM_MODE": DM_MODE,
"TOKEN_TIMEOUT": TOKEN_TIMEOUT}




BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    error("BOT_TOKEN variable is missing! Exiting now")
    LOGGER.error
    exit(1)

    

bot_id = BOT_TOKEN.split(':', 1)[0]




COLLECTION_NAME = environ.get('COLLECTION_NAME', '')
DATABASE_URL = environ.get('DATABASE_URL', '')
DATABASE_NAME = environ.get('DATABASE_NAME', '')



