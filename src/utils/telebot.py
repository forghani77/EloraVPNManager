import json
from typing import List

from pydantic import BaseModel

from src.utils.exc import InvalidJSONFormatError
from telebot import types


class Keyboard(BaseModel):
    text: str
    callback_data: str = None
    url: str = None

    def to_json(self):
        return {"text": self.text, "callback_data": self.callback_data, "url": self.url}


class KeyboardFactory:
    @staticmethod
    def from_keyboard(keyboards: List[Keyboard]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        buttons = []
        for keyboard in keyboards:
            args = {"text": keyboard.text}
            if keyboard.url:
                args["url"] = keyboard.url
            if keyboard.callback_data:
                args["callback_data"] = keyboard.callback_data
            buttons.append(types.InlineKeyboardButton(**args))

        for i in range(0, len(buttons), 2):
            markup.row(*buttons[i : i + 2])
        return markup

    @staticmethod
    def from_json_string(keyboards_input) -> types.InlineKeyboardMarkup:
        """
        Creates an InlineKeyboardMarkup from a JSON string or a list of keyboard dictionaries.
        """
        if not keyboards_input:
            return types.InlineKeyboardMarkup()

        if isinstance(keyboards_input, str):
            try:
                keyboards_list = json.loads(keyboards_input)
            except json.JSONDecodeError:
                raise InvalidJSONFormatError()
        else:
            keyboards_list = keyboards_input

        markup = types.InlineKeyboardMarkup()

        buttons = []
        for keyboard_dict in keyboards_list:
            args = {}
            if "text" in keyboard_dict:
                args["text"] = keyboard_dict["text"]
            if "url" in keyboard_dict and keyboard_dict["url"]:
                args["url"] = keyboard_dict["url"]
            if "callback_data" in keyboard_dict and keyboard_dict["callback_data"]:
                args["callback_data"] = keyboard_dict["callback_data"]

            if "text" in args:
                buttons.append(types.InlineKeyboardButton(**args))

        for i in range(0, len(buttons), 2):
            markup.row(*buttons[i : i + 2])

        return markup
