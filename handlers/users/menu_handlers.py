from typing import Union
from datetime import datetime

from data.config import admins
from handlers.users.aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.user_keyboards import *

from keyboards.inline.reject_accept import accept_reject, accept_reject_en, accept_reject_uz
from keyboards.inline.service_menu_keyboard import *
from keyboards.inline.user_keyboards import *
from keyboards.user_keyboard import user_start_keyboard, user_start_keyboard_en, \
    user_start_keyboard_uz
from loader import dp, bot
from utils.db_api.calendar_commands import get_available_hours, set_nine, set_eleven, set_two, set_four, add_new_date
from utils.db_api.models import Calendar
from utils.db_api.reservation_commands import add_reservation, get_id_by_code, get_user_by_reservation_id, \
    accept_reservation, delete_reservation, delete_from_calendar
from utils.db_api.service_commands import *
from utils.db_api.customer_commads import *

current_year: int = datetime.now().year
current_month: int = datetime.now().month
current_day: int = datetime.now().day

class Auth(StatesGroup):
    name = State()
    phone = State()
    date = State()
    time = State()
    service = State()
    confirmed = State()



# Хендлер на команду /menu
@dp.message_handler(Command("services"))
@dp.message_handler(text="⚙Сервисы")
@dp.message_handler(text="⚙Servislar")
@dp.message_handler(text="⚙Services")
async def show_menu(message: types.Message):
    # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
    await list_categories(message)



async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    lang = await get_language(message.from_user.id)
    markup = await categories_keyboard(lang)

    if isinstance(message, Message):
        if lang == "ru":
            await message.answer("Выберите категорию", reply_markup=markup)
        if lang == "en":
            await message.answer("Choose category:", reply_markup=markup)
        if lang == "uz":
            await message.answer("Kategoriyani tanlang:", reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    lang = await get_language(callback.from_user.id)
    markup = await subcategories_keyboard(category, lang)

    await callback.message.edit_reply_markup(markup)


async def list_services(callback: CallbackQuery, category, subcategory, **kwargs):
    lang = await get_language(callback.from_user.id)
    markup = await services_keyboard(category, subcategory, lang)

    if lang == "ru": text1 = "Выберите сервис:"
    if lang == "en": text1 = "Choose service:"
    if lang == "uz": text1 = "Servisni tanlang:"
    await callback.message.edit_text(text=text1, reply_markup=markup)


# Функция, которая отдает уже кнопку Купить товар по выбранному товару
async def show_service(callback: CallbackQuery, category, subcategory, service_id):
    lang = await get_language(callback.from_user.id)
    markup = service_keyboard(category, subcategory, service_id, lang)

    # Берем запись о нашем товаре из базы данных
    service = await get_service(service_id)
    if lang == "ru": text1 = f"Получить сервис '{translate(service.name, 'ru')}'"
    if lang == "en": text1 = f"Get service '{translate(service.name, 'en')}'"
    if lang == "uz": text1 = f"Servisga buyurtma berish: '{translate(service.name, 'uz')}'"
    await callback.message.edit_text(text=text1, reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    current_level = callback_data.get("level")

    category = callback_data.get("category")

    subcategory = callback_data.get("subcategory")

    service_id = int(callback_data.get("service_id"))

    levels = {
        "0": list_categories,  # Отдаем категории
        "1": list_subcategories,  # Отдаем подкатегории
        "2": list_services,  # Отдаем товары
        "3": show_service  # Предлагаем купить товар
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        category=category,
        subcategory=subcategory,
        service_id=service_id
    )



#@dp.message_handler(commands=["cancel"], state="*")
@dp.message_handler(text="Отменить❌", state="*")
@dp.message_handler(text="Bekor qilish❌", state="*")
@dp.message_handler(text="Cancel❌", state="*")
async def cancel_reservation(message: types.Message, state=FSMContext):
    lang = await get_language(message.from_user.id)
    await state.reset_state(with_data=True)
    if lang == "ru":
        await message.answer(text="Отменено!", reply_markup=user_start_keyboard)
    elif lang == "en":
        await message.answer(text="Canceled!", reply_markup=user_start_keyboard_en)
    elif lang == "uz":
        await message.answer(text="Bekor qilindi!", reply_markup=user_start_keyboard_uz)

@dp.callback_query_handler(text_startswith='buy')
async def auth_user(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_language(callback.from_user.id)

    text = callback.message.text
    await state.reset_state(with_data=True)
    if lang == "ru":
        service = callback.message.text[17:-1]
    if lang == "uz":
        service = callback.message.text[27:-1]
    if lang == "en":
        service = callback.message.text[13:-1]

    await state.update_data(service=service)
    await callback.message.delete()

    if lang == "ru":
        text1 = "Введите имя"
        markup = cancel_keyboard
    if lang == "en":
        text1 = "Enter your name"
        markup = cancel_keyboard_en
    if lang == "uz":
        text1 = "Ismingizni kiriting"
        markup = cancel_keyboard_uz
    await callback.message.answer(text=text1, reply_markup=markup)
    await Auth.name.set()


@dp.message_handler(state=Auth.name)
async def get_name(message: types.Message, state=FSMContext):
    lang = await get_language(message.from_user.id)
    name = message.text
    if name.isdigit():
        await message.reply(text=translate("❗Введите правильное значение!", lang))
    else:
        await state.update_data(name=name)
        await message.answer(text=translate("📅Выберите дату", lang),
                             reply_markup=(await SimpleCalendar().start_calendar()))
        await Auth.date.set()

@dp.callback_query_handler(simple_cal_callback.filter(), state=Auth.date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state=FSMContext):
    lang = await get_language(callback_query.from_user.id)
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        selected_date = f'{date.strftime("%Y/%m/%d")}'
        day = int(selected_date.split('/')[2])
        month = int(selected_date.split('/')[1])
        year = int(selected_date.split('/')[0])

        dddate = await Calendar.query.where(Calendar.date == selected_date).gino.first()
        if dddate == None:
            await add_new_date(selected_date)

        if year < current_year:
            await callback_query.answer(text=translate("Указана неверная дата", lang), show_alert=True)
            #await callback_query.message.edit_text(text="Выберите правильную дату", reply_markup=SimpleCalendar().start_calendar())
            await callback_query.message.answer(text=translate("📅Выберите правильную дату", lang),
                                                reply_markup=await SimpleCalendar().start_calendar())

        elif current_year == year:
            if month < current_month:
                await callback_query.answer(text=translate("Указана неверная дата", lang), show_alert=True)
                await callback_query.message.answer(text=translate("📅Выберите правильную дату", lang),
                                                    reply_markup=await SimpleCalendar().start_calendar())

            elif month == current_month:
                if day < current_day:
                    await callback_query.answer(text=translate("Указана неверная дата", lang) ,show_alert=True)
                    await callback_query.message.answer(text=translate("📅Выберите правильную дату", lang),
                                                        reply_markup=await SimpleCalendar().start_calendar())

                elif day == current_day:
                    await callback_query.answer(
                        text=translate("Нет свободных часов🕑\nВыберите другую дату", lang), show_alert=True)
                    await callback_query.message.answer(text=translate("📅Выберите правильную дату", lang),
                                                        reply_markup=await SimpleCalendar().start_calendar())

                else:
                    new_date = f'{date.strftime("%Y/%m/%d")}'

                    hours_button = InlineKeyboardMarkup()

                    arr = await get_available_hours(new_date)

                    if "Available" not in arr:
                        await callback_query.answer(
                            text=translate("Нет свободных часов🕑\nВыберите другую дату", lang), show_alert=True)
                        await callback_query.message.answer(text=translate("📅Выберите дату", lang),
                                                            reply_markup=await SimpleCalendar().start_calendar())


                    else:

                        if arr[0] == 'Available':
                            hours_button.row(
                                InlineKeyboardButton(
                                    text="09:00", callback_data="time_09:00"))

                        if arr[1] == 'Available':
                            hours_button.row(
                                InlineKeyboardButton(
                                    text="11:00", callback_data="time_11:00"))
                        if arr[2] == 'Available':
                            hours_button.row(
                                InlineKeyboardButton(
                                    text="14:00", callback_data="time_14:00"))
                        if arr[3] == 'Available':
                            hours_button.row(
                                InlineKeyboardButton(
                                    text="16:00", callback_data="time_16:00"))

                        await state.update_data(date=f'{date.strftime("%Y/%m/%d")}')


                        await callback_query.message.edit_text(text=translate("🕑Выберите время:", lang),
                                                                       reply_markup=hours_button)
                        await Auth.time.set()

        else:

            await state.update_data(date=f'{date.strftime("%Y/%m/%d")}')
            new_date = f'{date.strftime("%Y/%m/%d")}'

            hours_button = InlineKeyboardMarkup()
            arr = await get_available_hours(new_date)

            if "Available" not in arr:
                await callback_query.answer(
                    text=translate("Нет свободных часов🕑\nВыберите другую дату", lang), show_alert=True)
                await callback_query.message.answer(text=translate("📅Выберите дату", lang),
                                                    reply_markup=await SimpleCalendar().start_calendar())
                await Auth.time.set()

            if arr[0] == 'Available':
                hours_button.row(
                    InlineKeyboardButton(
                        text="09:00", callback_data="time_09:00"))

            if arr[1] == 'Available':
                hours_button.row(
                    InlineKeyboardButton(
                        text="11:00", callback_data="time_11:00"))
            if arr[2] == 'Available':
                hours_button.row(
                    InlineKeyboardButton(
                        text="14:00", callback_data="time_14:00"))
            if arr[3] == 'Available':
                hours_button.row(
                    InlineKeyboardButton(
                        text="16:00", callback_data="time_16:00"))

            await state.update_data(date=f'{date.strftime("%Y/%m/%d")}')
            #await callback_query.message.edit_reply_markup() #deleting keyboard
            await callback_query.message.answer(text=translate('Вы выбрали ', lang) + date.strftime("%Y/%m/%d"))
            await callback_query.message.answer(text=translate("🕑Выберите время:", lang), reply_markup=hours_button)
            await Auth.time.set()




@dp.callback_query_handler(state=Auth.time, text="time_09:00")
async def get_time(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_language(callback.from_user.id)
    await callback.answer()
    time = '09:00'
    await state.update_data(time=time)
    await callback.message.answer(translate("Отправьте номер телефона", lang), reply_markup=get_phone_keyboard(lang))

    await Auth.phone.set()


@dp.callback_query_handler(state=Auth.time, text="time_11:00")
async def get_time(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_language(callback.from_user.id)
    await callback.answer()
    time = '11:00'
    await state.update_data(time=time)
    await callback.message.answer(translate("Отправьте номер телефона", lang), reply_markup=get_phone_keyboard(lang))

    await Auth.phone.set()


@dp.callback_query_handler(state=Auth.time, text="time_14:00")
async def get_time(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_language(callback.from_user.id)
    await callback.answer()
    time = '14:00'
    await state.update_data(time=time)
    await callback.message.answer(translate("Отправьте номер телефона", lang), reply_markup=get_phone_keyboard(lang))
    await Auth.phone.set()


@dp.callback_query_handler(state=Auth.time, text="time_16:00")
async def get_time(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_language(callback.from_user.id)
    await callback.answer()
    time = '16:00'
    await state.update_data(time=time)
    await callback.message.answer(translate("Отправьте номер телефона", lang), reply_markup=get_phone_keyboard(lang))

    await Auth.phone.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Auth.phone)
async def get_phone(message: types.Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    data = await state.get_data()
    price = await get_price(data.get('service'))
    if lang == "ru":
        msg = f"Сервис:    {data.get('service')}\n"\
                f"Имя:     {data.get('name')}\n"\
                f"Дата:    {data.get('date')}\n"\
                f"Время:   {data.get('time')}\n"\
                f"Телефон: {data.get('phone')}\n"\
                f"Цена:    {price}$"
        await message.answer(text="Так выглядят данные вашего заказа📝\n"\
                                    "Если все ОК, нажмите 'Подтвердить'", reply_markup=cancel_keyboard)

    elif lang == "en":
        price = await get_price_en(data.get('service'))
        msg = f"Service:    {data.get('service')}\n" \
              f"Name:     {data.get('name')}\n" \
              f"Date:    {data.get('date')}\n" \
              f"Time:   {data.get('time')}\n" \
              f"Phone: {data.get('phone')}\n" \
              f"Cost:    {price}$"
        await message.answer(text="All data of your order looks like this📝\n" \
                                  "If everything is ОК, press 'Confirm'", reply_markup=cancel_keyboard_en)

    elif lang == "uz":
        price = await get_price_uz(data.get('service'))
        msg = f"Servis:    {data.get('service')}\n" \
              f"Ism:     {data.get('name')}\n" \
              f"Sana:    {data.get('date')}\n" \
              f"Vaqt:   {data.get('time')}\n" \
              f"Tel: {data.get('phone')}\n" \
              f"Narx:    {price}$"
        await message.answer(text="Buyurtmangizning malumotlari shunday ko'rinishda📝\n" \
                                  "Hammasi ОК bo`lsa, 'Tasdiqlash'ni bosing", reply_markup=cancel_keyboard_uz)

    await message.answer(msg, reply_markup=confirm_keyboard_button(lang))
    await Auth.confirmed.set()

@dp.callback_query_handler(text="confirm_reservation", state=Auth.confirmed)
async def confirm_res(callback=types.CallbackQuery, state=FSMContext):
    lang = await get_language(callback.from_user.id)
    await callback.answer()
    await state.update_data(confirmed=True)
    data = await state.get_data()
    if lang == "ru": price = await get_price(data.get('service'))
    if lang == "en": price = await get_price_en(data.get('service'))
    if lang == "uz": price = await get_price_uz(data.get('service'))

    code = f"{callback.from_user.id}{data.get('date')}{data.get('time')}"
    await add_reservation(
        customer_name=data.get('name'),
        customer_id=callback.from_user.id,
        customer_phone=data.get('phone'),
        service=data.get('service'),
        date=data.get('date'),
        time=data.get('time'),
        price=price,
        code=f"{callback.from_user.id}{data.get('date')}{data.get('time')}",
        accepted=0
    )
    if data.get('time') == '09:00':
        await set_nine(data.get('date'))
    if data.get('time') == '11:00':
        await set_eleven(data.get('date'))
    if data.get('time') == '14:00':
        await set_two(data.get('date'))
    if data.get('time') == '16:00':
        await set_four(data.get('date'))
    id = await get_id_by_code(code)
    adlang = await get_language(int(admins[0]))
    if adlang == "ru":
        await bot.send_message(chat_id=admins[0],
                               text=f"📣НОВЫЙ ЗАКАЗ!!!\n\n"
                                    f"📝ID: {id}\n"
                                    f"🔧Сервис: {data.get('service')}\n"
                                    f"👤Имя клиента: {data.get('name')}\n"
                                    f"📞Номер: {data.get('phone')}\n"
                                    f"📅Дата: {data.get('date')}\n"
                                    f"🕑Время: {data.get('time')}\n"
                                    f"💵Цена: {price}", reply_markup=accept_reject)
    if adlang == "en":
        await bot.send_message(chat_id=admins[0],
                               text=f"📣NEW ORDER!!!\n\n"
                                    f"📝ID: {id}\n"
                                    f"🔧Service: {data.get('service')}\n"
                                    f"👤Name: {data.get('name')}\n"
                                    f"📞Phone number: {data.get('phone')}\n"
                                    f"📅Date: {data.get('date')}\n"
                                    f"🕑Time: {data.get('time')}\n"
                                    f"💵Price: {price}", reply_markup=accept_reject_en)

    if adlang == "uz":
        await bot.send_message(chat_id=admins[0],
                               text=f"📣YANGI BUYURTMA!!!\n\n"
                                    f"📝ID: {id}\n"
                                    f"🔧Servis: {data.get('service')}\n"
                                    f"👤Ism: {data.get('name')}\n"
                                    f"📞Nomer: {data.get('phone')}\n"
                                    f"📅Sana: {data.get('date')}\n"
                                    f"🕑Vaqt: {data.get('time')}\n"
                                    f"💵Narx: {price}", reply_markup=accept_reject_uz)

    lang = await get_language(callback.from_user.id)
    if lang == "en": markup = user_start_keyboard_en
    if lang == "ru": markup = user_start_keyboard
    if lang == "uz": markup = user_start_keyboard_uz
    await callback.message.answer(text=translate("Ваш запрос принят", lang), reply_markup=markup)

    await state.reset_state(with_data=True)

@dp.callback_query_handler(text="accept_order")
async def accept_order(callback: types.CallbackQuery):
    await callback.answer(text=translate("Заказ принят", await get_language(callback.from_user.id)))
    await callback.answer()
    id = int(callback.message.text.split()[3])
    user_id = await get_user_by_reservation_id(id)
    await accept_reservation(id)
    await bot.send_message(chat_id=user_id, text=translate("Ваш заказ принят✅", await get_language(user_id)))


@dp.callback_query_handler(text="reject_order")
async def reject_order(callback: types.CallbackQuery):
    await callback.answer(text="Заказ отклонен")
    await callback.answer()
    id = int(callback.message.text.split()[3])
    user_id = await get_user_by_reservation_id(id)
    await delete_from_calendar(id)
    await delete_reservation(id)
    await bot.send_message(chat_id=user_id, text=translate("Простите ваш заказ отклонен😔", await get_language(user_id)))



