from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


start_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
language_button = KeyboardButton(text="🌐Bыбpaть язык")
reservations = KeyboardButton(text="⚙Закaзы")
available_days = KeyboardButton(text="💤Cвoбoдныe дни")
admin_comments_keyboard = KeyboardButton(text="✍Отзывы")
web_interface_keyboard = KeyboardButton(text="🖥Веб-интерфейс")


start_button.row(reservations)
start_button.row(available_days, admin_comments_keyboard)
start_button.row(language_button, web_interface_keyboard)


###ENGLISH
start_button_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
language_button = KeyboardButton(text="🌐Choose lаnguage")
reservations = KeyboardButton(text="⚙Orders")
available_days = KeyboardButton(text="💤Schedule")
admin_comments_keyboard = KeyboardButton(text="✍Reviews")
web_interface_keyboard = KeyboardButton(text="🖥Web-iterface")


start_button_en.row(reservations)
start_button_en.row(available_days, admin_comments_keyboard)
start_button_en.row(language_button, web_interface_keyboard)


#UZBEK
start_button_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
language_button = KeyboardButton(text="🌐Tilni tаnlash")
reservations = KeyboardButton(text="⚙Buyurtmalar")
available_days = KeyboardButton(text="💤Bo'sh kunlar")
admin_comments_keyboard = KeyboardButton(text="✍Kommentariylar")
web_interface_keyboard = KeyboardButton(text="🖥Web-iterfeys")

start_button_uz.row(reservations)
start_button_uz.row(available_days, admin_comments_keyboard)
start_button_uz.row(language_button, web_interface_keyboard)





