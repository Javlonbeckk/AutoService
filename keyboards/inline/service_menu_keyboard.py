from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.service_commands import *

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "service_id")
buy_item = CallbackData("buy", "service_id")
from keyboards.inline.dictionary import translate

# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="0", subcategory="0", service_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, service_id=service_id)



# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def categories_keyboard(lang):
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    categories = await get_categories()
    for category in categories:
        button_text = f"{category.category_name}"
        button_text = translate(button_text, lang)

        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)

        # Вставляем кнопку в клавиатуру
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными подкатегориями, исходя из выбранной категории
async def subcategories_keyboard(category, lang):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    # Забираем список товаров с РАЗНЫМИ подкатегориями из базы данных с учетом выбранной категории и проходим по ним
    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        # Чекаем в базе сколько товаров существует под данной подкатегорией
        #number_of_items = await count_items(category_code=category, subcategory_code=subcategory.subcategory_code)

        # Сформируем текст, который будет на кнопке
        button_text = f"{subcategory.subcategory_name}"
        button_text = translate(button_text, lang)

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, subcategory=subcategory.subcategory_code)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )


    if lang == "en":
        text2 = f"⬅Go Back"
    if lang == "ru":
        text2 = f"⬅Назад"
    if lang == "uz":
        text2 = f"⬅Orqaga"
    markup.row(
        InlineKeyboardButton(
            text=text2,
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными сервисами, исходя из выбранной категории и подкатегории
async def services_keyboard(category, subcategory, lang):
    CURRENT_LEVEL = 2

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на сервис
    markup = InlineKeyboardMarkup(row_width=1)

    # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
    services = await get_services(category, subcategory)
    for service in services:
        servicename = translate(service.name, lang)
        button_text = f"{servicename} - ${service.price}"

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, subcategory=subcategory,
                                           service_id=service.id)
        markup.row(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
    markup.row(
        InlineKeyboardButton(
            text="⬅Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "получить сервис" и "назад" для выбранного сервиса
def service_keyboard(category, subcategory, service_id, lang):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    if lang == "en":
        text1 = f"Get service"
        text2 = f"⬅Go Back"
    if lang == "ru":
        text1 = f"Получить сервис"
        text2 = f"⬅Назад"
    if lang == "uz":
        text1 = f"Servisni olish"
        text2 = f"⬅Orqaga"
    markup.row(
        InlineKeyboardButton(
            text=text1,
            callback_data='buy'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=text2,
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category, subcategory=subcategory))
    )
    return markup
