from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.dictionary import translate

def confirm_keyboard_button(lang):
    confirm_keyboard = InlineKeyboardMarkup()
    confirm_keyboard.row(
            InlineKeyboardButton(text=translate("Подтвердить☑", lang),
                                 callback_data="confirm_reservation")
        )
    return confirm_keyboard
