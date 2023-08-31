from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ButtonMaker:
    def __init__(self):
        self.__button = []
        self.__header_button = []
        self.__footer_button = []

    def ubutton(self, key, link, position=None):
        if not position:
            self.__button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'header':
            self.__header_button.append(
                InlineKeyboardButton(text=key, url=link))
        elif position == 'footer':
            self.__footer_button.append(
                InlineKeyboardButton(text=key, url=link))