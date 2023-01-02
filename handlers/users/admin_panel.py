import datetime

from data.config import admins
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.admin_keyboard import start_button, start_button_uz, start_button_en
from loader import dp
from utils.db_api.calendar_commands import get_available_hours
from utils.db_api.reservation_commands import show_reservations, show_comments
from utils.db_api.customer_commads import *


@dp.message_handler(user_id=admins[0], commands=["start"])
async def privet(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    userid = await User.select('user_id').where(
        User.user_id == user_id).gino.scalar()
    if userid == None:
        await add_customer(user_id=user_id, username=username, fullname=fullname)

    if await get_language(userid) == "ru":
        await message.answer(text="👋Привет админ", reply_markup=start_button)
    if await get_language(userid) == "uz":
        await message.answer(text="👋Assalomu alaykum", reply_markup=start_button_uz)
    if await get_language(userid) == "en":
        await message.answer(text="👋Hi admin", reply_markup=start_button_en)

@dp.message_handler(user_id=admins[0], text="🌐Choose lаnguage")
@dp.message_handler(user_id=admins[0], text="🌐Tilni tаnlash")
@dp.message_handler(user_id=admins[0], text="🌐Bыбрaть язык")
@dp.message_handler(user_id=admins[0], commands=['language'])
async def change_language(message: types.Message):
    languages_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)

    lang_en = KeyboardButton("🇬🇧Еnglish")
    lang_ru = KeyboardButton("🇷🇺Рyсский")
    lang_uz = KeyboardButton("🇺🇿O`zbеk")
    languages_markup.row(lang_en, lang_ru, lang_uz)
    if await get_language(message.from_user.id) == 'ru':
        await message.answer("Выберите язык: ", reply_markup=languages_markup)
    if await get_language(message.from_user.id) == 'en':
        await message.answer("Choose language: ", reply_markup=languages_markup)
    if await get_language(message.from_user.id) == 'uz':
        await message.answer("Tilni tanlang: ", reply_markup=languages_markup)



@dp.message_handler(user_id=admins[0], text="🇬🇧Еnglish")
async def change_to_english(message: types.Message):
    #await call.message.edit_reply_markup()
    language = message.text
    msg = "You have selected English"
    new_language = "en"
    await message.answer(msg, reply_markup=start_button_en)
    await set_language(message.from_user.id, new_language)

@dp.message_handler(user_id=admins[0], text="🇷🇺Рyсский")
async def change_to_english(message: types.Message):
    language = message.text
    userid = message.from_user.id
    msg = "Вы выбрали русский язык"
    new_language = "ru"
    await message.answer(msg, reply_markup=start_button)
    await set_language(message.from_user.id, new_language)

@dp.message_handler(user_id=admins[0], text="🇺🇿O`zbеk")
async def change_to_english(message: types.Message):
    msg = "Siz ozbek tilini tanladingiz"
    new_language = "uz"
    await message.answer(msg, reply_markup=start_button_uz)
    await set_language(message.from_user.id, new_language)

@dp.message_handler(user_id=admins[0], text="⚙Закaзы")
@dp.message_handler(user_id=admins[0], text="⚙Orders")
@dp.message_handler(user_id=admins[0], text="⚙Buyurtmalar")
async def show_books(message: types.Message):
    reservations = await show_reservations()
    if reservations == []:
        if await get_language(message.from_user.id) == "ru":
            await message.answer(text="У вас пока нет заказов.", reply_markup=start_button)
        if await get_language(message.from_user.id) == "en":
            await message.answer(text="You don't have any orders.", reply_markup=start_button_en)
        if await get_language(message.from_user.id) == "uz":
            await message.answer(text="Sizda buyurtmalar mavjud emas.", reply_markup=start_button_uz)
    for reservation in reservations:
        if await get_language(message.from_user.id) == "ru":
            await message.answer(
                text=f"🔧Сервис:        {reservation.service}\n"
                     f"👤Имя клиента:   {reservation.customer_name}\n"
                     f"📞Номер клиента: {reservation.customer_phone}\n"
                     f"📆Дата:          {reservation.date}\n"
                     f"🕑Время:         {reservation.time}\n"
                     f"💸Цена:           {reservation.price}\n", reply_markup=start_button)

        if await get_language(message.from_user.id) == "en":
            await message.answer(
                text=f"🔧Service: {reservation.service}\n"
                f"👤Name of client: {reservation.customer_name}\n"
                f"📞Phone: {reservation.customer_phone}\n"
                f"📆Date: {reservation.date}\n"
                f"🕑Time: {reservation.time}\n"
                f"💸Cost: {reservation.price}\n", reply_markup=start_button_en)

        if await get_language(message.from_user.id) == "uz":
            await message.answer(
                text=f"🔧Servis: {reservation.service}\n"
                f"👤Mijoz ismi: {reservation.customer_name}\n"
                f"📞Tel: {reservation.customer_phone}\n"
                f"📆Data: {reservation.date}\n"
                f"🕑Vaqt: {reservation.time}\n"
                f"💸Narx: {reservation.price}\n", reply_markup=start_button_uz)

@dp.message_handler(user_id=admins[0], text="💤Cвoбoдныe дни")
@dp.message_handler(user_id=admins[0], text="💤Schedule")
@dp.message_handler(user_id=admins[0], text="💤Bo'sh kunlar")
async def show_free_days(message: types.Message):
    today = datetime.datetime.now()
    delta1 = datetime.timedelta(days=1)
    delta2 = datetime.timedelta(days=2)
    delta3 = datetime.timedelta(days=3)
    delta4 = datetime.timedelta(days=4)
    delta5 = datetime.timedelta(days=5)
    delta6 = datetime.timedelta(days=6)

    date0 = today
    date1 = today + delta1
    date2 = today + delta2
    date3 = today + delta3
    date4 = today + delta4
    date5 = today + delta5
    date6 = today + delta6


    if date0.month < 10:
        sdate0 = f"{date0.year}/0{date0.month}/"
    else:
        sdate0 = f"{date0.year}/{date0.month}/"
    if date0.day < 10:
        sdate0 += f"0{date0.day}"
    else:
        sdate0 += f"{date0.day}"

    if date1.month < 10:
        sdate1 = f"{date1.year}/0{date1.month}/"
    else:
        sdate1 = f"{date1.year}/{date1.month}/"
    if date0.day < 10:
        sdate1 += f"0{date1.day}"
    else:
        sdate1 += f"{date1.day}"

    if date2.month < 10:
        sdate2=f"{date2.year}/0{date2.month}/"
    else:
        sdate2 = f"{date2.year}/{date2.month}/"
    if date2.day < 10:
        sdate2 += f"0{date2.day}"
    else:
        sdate2 += f"{date2.day}"

    if date3.month < 10:
        sdate3 = f"{date3.year}/0{date3.month}/"
    else:
        sdate3 = f"{date3.year}/{date3.month}/"
    if date3.day < 10:
        sdate3 += f"0{date3.day}"
    else:
        sdate3 += f"{date3.day}"

    if date4.month < 10:
        sdate4=f"{date4.year}/0{date4.month}/"
    else:
        sdate4 = f"{date4.year}/{date4.month}/"
    if date4.day < 10:
        sdate4 += f"0{date4.day}"
    else:
        sdate4 += f"{date4.day}"

    if date5.month < 10:
        sdate5 = f"{date5.year}/0{date5.month}/"
    else:
        sdate5 = f"{date5.year}/{date5.month}/"
    if date5.day < 10:
        sdate5 += f"0{date5.day}"
    else:
        sdate5 += f"{date5.day}"

    if date6.month < 10:
        sdate6=f"{date6.year}/0{date6.month}/"
    else:
        sdate6 = f"{date6.year}/{date6.month}/"
    if date6.day < 10:
        sdate6 += f"0{date6.day}"
    else:
        sdate6 += f"{date6.day}"

    timetable_day0 = await get_available_hours(sdate0)
    timetable_day1 = await get_available_hours(sdate1)
    timetable_day2 = await get_available_hours(sdate2)
    timetable_day3 = await get_available_hours(sdate3)
    timetable_day4 = await get_available_hours(sdate4)
    timetable_day5 = await get_available_hours(sdate5)
    timetable_day6 = await get_available_hours(sdate6)


    async def is_free(arr, i):
        if arr[i] == "Available" or arr[i] == None:
            if await get_language(message.from_user.id) == "ru":
                return "Вы свободны💤"
            if await get_language(message.from_user.id) == "en":
                return "You are free💤"
            if await get_language(message.from_user.id) == "uz":
                return "Siz bo'shsiz💤"
        else:
            if await get_language(message.from_user.id) == "ru":
                return "🔧Есть заказ"
            if await get_language(message.from_user.id) == "en":
                return "🔧You have a work"
            if await get_language(message.from_user.id) == "uz":
                return "🔧Buyurtma bor"

    if await get_language(message.from_user.id) == "ru":
        tekst = "РАСПИСАНИЕ ДЛЯ СЛЕДУЮЩИХ 7 ДНЕЙ:\n\n"
    if await get_language(message.from_user.id) == "uz":
        tekst = "KEYINGI 7 KUN UCHUN JADVAL:\n\n"
    if await get_language(message.from_user.id) == "en":
        tekst = "SCHEDULE FOR THE NEXT 7 DAYS:\n\n"

    text = tekst + f"{sdate0}\n" \
        f"09:00-11:00 — {await is_free(timetable_day0, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day0, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day0, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day0, 3)}\n\n" \
        f"{sdate1}\n" \
        f"09:00-11:00 — {await is_free(timetable_day1, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day1, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day1, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day1, 3)}\n\n" \
        f"{sdate2}\n" \
        f"09:00-11:00 — {await is_free(timetable_day2, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day2, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day2, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day2, 3)}\n\n" \
        f"{sdate3}\n" \
        f"09:00-11:00 — {await is_free(timetable_day3, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day3, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day3, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day3, 3)}\n\n" \
        f"{sdate4}\n" \
        f"09:00-11:00 — {await is_free(timetable_day4, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day4, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day4, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day4, 3)}\n\n" \
        f"{sdate5}\n" \
        f"09:00-11:00 — {await is_free(timetable_day5, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day5, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day5, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day5, 3)}\n\n" \
        f"{sdate6}\n" \
        f"09:00-11:00 — {await is_free(timetable_day6, 0)}\n" \
        f"11:00-13:00 — {await is_free(timetable_day6, 1)}\n" \
        f"14:00-16:00 — {await is_free(timetable_day6, 2)}\n" \
        f"16:00-18:00 — {await is_free(timetable_day6, 3)}\n\n"
    if await get_language(message.from_user.id) == "ru":
        await message.answer(text=text, reply_markup=start_button)
    if await get_language(message.from_user.id) == "en":
        await message.answer(text=text, reply_markup=start_button_en)
    if await get_language(message.from_user.id) == "uz":
        await message.answer(text=text, reply_markup=start_button_uz)

@dp.message_handler(user_id=admins[0], text="✍Отзывы")
@dp.message_handler(user_id=admins[0], text="✍Reviews")
@dp.message_handler(user_id=admins[0], text="✍Kommentariylar")
async def get_comments(message: types.Message):
    comments = await show_comments()
    if comments == []:
        if await get_language(message.from_user.id) == "ru":
            await message.answer(text="У вас пока нет отзывов", reply_markup=start_button)
        if await get_language(message.from_user.id) == "en":
            await message.answer(text="You do not have any reviews", reply_markup=start_button_en)
        if await get_language(message.from_user.id) == "uz":
            await message.answer(text="Sizda hozircha kommentariylar yo'q", reply_markup=start_button_uz)
    for comment in comments:
        if await get_language(message.from_user.id) == "ru":
            await message.answer(
                text = f"📅Дата:       {comment.date}\n"\
                       f"👤ID клиента: {comment.user_id}\n"\
                       f"💬Отзыв:      {comment.comment}\n",
                reply_markup=start_button)
        if await get_language(message.from_user.id) == "uz":
            await message.answer(
                text = f"📅Data:             {comment.date}\n"\
                       f"👤Mijoz IDsi:       {comment.user_id}\n"\
                       f"💬Kommentariy:      {comment.comment}\n",
                reply_markup=start_button_uz)
        if await get_language(message.from_user.id) == "en":
            await message.answer(
                text = f"📅Date:       {comment.date}\n"\
                       f"👤ID of client: {comment.user_id}\n"\
                       f"💬Review:      {comment.comment}\n",
                reply_markup=start_button_en)

@dp.message_handler(user_id=admins[0], text="🖥Веб-интерфейс")
@dp.message_handler(user_id=admins[0], text="🖥Web-iterface")
@dp.message_handler(user_id=admins[0], text="🖥Web-iterfeys")
async def get_comments(message: types.Message):
    lang = await get_language(message.from_user.id)
    if lang == "ru":
        await message.answer(text="http://127.0.0.1:5000", reply_markup=start_button)
    if lang == "uz":
        await message.answer(text="http://127.0.0.1:5000", reply_markup=start_button_uz)
    if lang == "en":
        await message.answer(text="http://127.0.0.1:5000", reply_markup=start_button_en)




