from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#START
user_start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

change_language = KeyboardButton(text="🌐Bыбpaть язык")
my_reservations = KeyboardButton(text="🛒Мои заказы")
all_services = KeyboardButton(text="⚙Сервисы")
contact_info_button = KeyboardButton(text="ℹИнформация")
cooperation_button = KeyboardButton(text="🤝Сотрудничество")

user_start_keyboard.row(all_services, my_reservations)
user_start_keyboard.row(cooperation_button, contact_info_button)
user_start_keyboard.row(change_language)

###Cancel Reservation
cancel_reservation_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
cancel_reservation_keyboard.add(KeyboardButton(text="Отменить❌"))

###
info_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
leave_comment = KeyboardButton(text="💬Оставить отзыв")
contacts_keyboard = KeyboardButton(text="☎Контакты")
main_menu = KeyboardButton(text="🏠Главное меню")

info_keyboard.row(leave_comment, contacts_keyboard)
info_keyboard.row(main_menu)


###ENGLISH
user_start_keyboard_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

change_language = KeyboardButton(text="🌐Choose language")
my_reservations = KeyboardButton(text="🛒My orders")
all_services = KeyboardButton(text="⚙Services")
contact_info_button = KeyboardButton(text="ℹContact info")
cooperation_button = KeyboardButton(text="🤝Cooperation")

user_start_keyboard_en.row(all_services, my_reservations)
user_start_keyboard_en.row(cooperation_button, contact_info_button)
user_start_keyboard_en.row(change_language)

###Cancel Reservation
cancel_reservation_keyboard_en = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
cancel_reservation_keyboard_en.add(KeyboardButton(text="Cancel❌"))

###
info_keyboard_en = ReplyKeyboardMarkup(resize_keyboard=True)
leave_comment = KeyboardButton(text="💬Leave comment")
contacts_keyboard = KeyboardButton(text="☎Contacts")
main_menu = KeyboardButton(text="🏠Main menu")

info_keyboard_en.row(leave_comment, contacts_keyboard)
info_keyboard_en.row(main_menu)



###UZBEK
user_start_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

change_language = KeyboardButton(text="🌐Tilni tanlash")
my_reservations = KeyboardButton(text="🛒Mening buyurtmalarim")
all_services = KeyboardButton(text="⚙Servislar")
contact_info_button = KeyboardButton(text="ℹInfo")
cooperation_button = KeyboardButton(text="🤝Hamkorlik")

user_start_keyboard_uz.row(all_services, my_reservations)
user_start_keyboard_uz.row(cooperation_button, contact_info_button)
user_start_keyboard_uz.row(change_language)

###Cancel Reservation
cancel_reservation_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
cancel_reservation_keyboard_uz.add(KeyboardButton(text="Bekor qilish❌"))

###
info_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True)
leave_comment = KeyboardButton(text="💬Kommentariy qoldirish")
contacts_keyboard = KeyboardButton(text="☎Kontaktlar")
main_menu = KeyboardButton(text="🏠Bosh menu")

info_keyboard_uz.row(leave_comment, contacts_keyboard)
info_keyboard_uz.row(main_menu)

