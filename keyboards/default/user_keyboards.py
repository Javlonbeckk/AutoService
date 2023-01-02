from aiogram import types

from keyboards.inline.dictionary import translate

cancel_keyboard_uz = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
cancel_keyboard_uz.add(types.KeyboardButton(text="Bekor qilish❌"))

cancel_keyboard_en = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
cancel_keyboard_en.add(types.KeyboardButton(text="Cancel❌"))

cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
cancel_keyboard.add(types.KeyboardButton(text="Отменить❌"))

def get_phone_keyboard(lang):
    phone_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone_keyboard.add(types.KeyboardButton(text=translate("☎Поделится контактом", lang), request_contact=True))
    return phone_keyboard