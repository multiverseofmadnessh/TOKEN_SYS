from os import environ
from time import time
from uuid import uuid4
from pyrogram import Client, filters
from infosys import DATABASE_URL, DATABASE_NAME, user_data, config_dict, DM_MODE, TOKEN_TIMEOUT
from db_handler import DbManager
from msg_utils import sendMessage, get_readable_time
from btn import ButtonMaker
from multishort import short_url


COLLECTION_NAME = environ.get('COLLECTION_NAME', '')
DATABASE_URI = environ.get('DATABASE_URI', '')
DATABASE_NAME = environ.get('DATABASE_NAME', '')

bot_name = "autodeletenewbot"
#TOKEN_TIMEOUT = int("60")  Replace with the actual token timeout in seconds

# Create a new Pyrogram client
SESSION = "TOKENBOT"  # Replace with your desired session name
API_ID = ""          # Replace with your actual API ID
API_HASH = ""      # Replace with your actual API hash
BOT_TOKEN = ""    # Replace with your actual bot token


# Create a new Pyrogram client
app = Client(
    name=SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# User data storage


@app.on_message(filters.private & filters.command("start"))
async def start(_, message):
    if len(message.command) > 1 and len(message.command[1]) == 36:
        userid = message.from_user.id
        input_token = message.command[1]
        if DATABASE_URL:
            stored_token = await DbManager().get_user_token(userid)
            if stored_token is None:
                return await sendMessage(message, 'This token is not associated with your account.\n\nPlease generate your own token.')
            if input_token != stored_token:
                return await sendMessage(message, 'Invalid token.\n\nPlease generate a new one.')
        if userid not in user_data:
            return await sendMessage(message, 'This token is not yours!\n\nKindly generate your own.')
        data = user_data[userid]
        if 'token' not in data or data['token'] != input_token:
            return await sendMessage(message, 'Token already used!\n\nKindly generate a new one.')
        token = str(uuid4())
        ttime = time()
        data['token'] = token
        data['time'] = ttime
        user_data[userid].update(data)
        if DATABASE_URL:
            await DbManager().update_user_tdata(userid, token, ttime)
        msg = 'Token refreshed successfully!\n\n'
        msg += f'Validity: {get_readable_time(int(config_dict["TOKEN_TIMEOUT"]))}'
        return await sendMessage(message, msg)
    elif config_dict['DM_MODE'] and message.chat.type != message.chat.type.SUPERGROUP:
        start_string = 'Bot Started.\n' \
                       'This is test token bot.'
    elif not config_dict['DM_MODE'] and message.chat.type != message.chat.type.SUPERGROUP:
        start_string = 'Sorry, you cannot use me here!\n' \
                       'This is test token bot.'
    else:
        tag = message.from_user.mention
        start_string = 'Start me in DM, not in the group.\n' \
                       f'cc: {tag}'
    await sendMessage(message, start_string)


app.on_message(filters.private & (filters.media | filters.video | filters.document) & filters.incoming)
async def checking_access(user_id, button=None):
    if not config_dict['TOKEN_TIMEOUT']:
        return None, button
    user_data.setdefault(user_id, {})
    data = user_data[user_id]
    if DATABASE_URL:
        data['time'] = await DbManager().get_token_expire_time(user_id)
    expire = data.get('time')
    isExpired = (expire is None or expire is not None and (time() - expire) > config_dict['TOKEN_TIMEOUT'])
    if isExpired:
        token = data['token'] if expire is None and 'token' in data else str(uuid4())
        if expire is not None:
            del data['time']
        data['token'] = token
        if DATABASE_URL:
            await DbManager().update_user_token(user_id, token)
        user_data[user_id].update(data)
        if button is None:
            button = ButtonMaker()
        button.ubutton('Get New Token', short_url(f'https://telegram.me/{bot_name}?start={token}'))
        tmsg = 'Your <b>Token</b> is expired. Get a new one.'
        tmsg += f'\n<b>Token Validity</b>: {get_readable_time(config_dict["TOKEN_TIMEOUT"])}'
        return tmsg, button
    return None, button




if __name__ == "__main__":
    app.run()
