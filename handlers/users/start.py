import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from data.config import admins
from keyboards.user_keyboard import user_start_keyboard, info_keyboard, user_start_keyboard_en, user_start_keyboard_uz, \
    info_keyboard_en, info_keyboard_uz
from utils.db_api.customer_commads import add_customer, set_language, get_language
from loader import dp, bot
from utils.db_api.models import User
from aiogram.dispatcher.filters.state import StatesGroup, State

from utils.db_api.reservation_commands import show_users_reservations, delete_reservation, add_comment


class Review(StatesGroup):
    comment = State()



@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    userid = await User.select('user_id').where(
        User.user_id == user_id).gino.scalar()
    if userid == None:
        await message.answer(f"Привет {fullname}\n"
                             f'Меню: /menu\n'
                             f'Выбрать язык: /language\n',
                             reply_markup=user_start_keyboard)
        await add_customer(user_id=user_id, username=username, fullname=fullname)

    else:
        if await get_language(userid) == 'ru':
            await message.answer(f'Привет, {message.from_user.full_name}! \n'
                                 f'Сервисы: /services\n'
                                 f'Выбрать язык: /language\n',
                                  reply_markup=user_start_keyboard)

        if await get_language(userid) == 'en':
            await message.answer(f'Hello, {message.from_user.full_name}! \n'
                                 f'Services:         /services\n'
                                 f'Choose language: /language\n',
                                  reply_markup=user_start_keyboard_en)

        if await get_language(userid) == 'uz':
            await message.answer(f'Assalomu alaykum, {message.from_user.full_name}! \n'
                                 f'Servislar:          /services\n'
                                 f'Tilni tanlash: /language\n',
                                  reply_markup=user_start_keyboard_uz)






@dp.message_handler(text="🌐Choose language")
@dp.message_handler(text="🌐Tilni tanlash")
@dp.message_handler(text="🌐Bыбpaть язык")
@dp.message_handler(commands=['language'])
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



@dp.message_handler(text="🇬🇧Еnglish")
async def change_to_english(message: types.Message):
    #await call.message.edit_reply_markup()
    language = message.text
    msg = "You have selected English"
    new_language = "en"
    await message.answer(msg, reply_markup=user_start_keyboard_en)
    await set_language(message.from_user.id, new_language)

@dp.message_handler(text="🇷🇺Рyсский")
async def change_to_english(message: types.Message):
    language = message.text
    userid = message.from_user.id
    msg = "Вы выбрали русский язык"
    new_language = "ru"
    await message.answer(msg, reply_markup=user_start_keyboard)
    await set_language(message.from_user.id, new_language)

@dp.message_handler(text="🇺🇿O`zbеk")
async def change_to_english(message: types.Message):
    msg = "Siz ozbek tilini tanladingiz"
    new_language = "uz"
    await message.answer(msg, reply_markup=user_start_keyboard_uz)
    await set_language(message.from_user.id, new_language)


@dp.message_handler(commands=["orders"])
@dp.message_handler(text="🛒Мои заказы")
@dp.message_handler(text="🛒My orders")
@dp.message_handler(text="🛒Mening buyurtmalarim")
async def show_my_reservaitions(message: types.Message):
    id_of_user = message.from_user.id
    my_reservations = await show_users_reservations(id_of_user)
    if my_reservations == []:
        if await get_language(message.from_user.id) == "ru":
            await message.answer(text="У вас пока нет заказов", reply_markup=user_start_keyboard)
        if await get_language(message.from_user.id) == "en":
            await message.answer(text="You do not have any orders", reply_markup=user_start_keyboard_en)
        if await get_language(message.from_user.id) == "uz":
            await message.answer(text="Sizda hali buyurtmalar yo'q", reply_markup=user_start_keyboard_uz)

    for reservation in my_reservations:
        res_id = reservation.id
        sdate = reservation.date
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        if day < 10:
            if month < 10:
                today = f"{year}/0{month}/0{day}"
            else:
                today = f"{year}/{month}/0{day}"
        else:
            if month < 10:
                today = f"{year}/0{month}/{day}"
            else:
                today = f"{year}/{month}/{day}"


        if sdate >= today:
            if await get_language(message.from_user.id) == "ru":
                delete_button = InlineKeyboardMarkup()
                delete_button.row(
                    InlineKeyboardButton(text="Удалить заказ",
                                         callback_data=f"delete_reservation{res_id}")
                )
                delete_button.row(
                    InlineKeyboardButton(text="⬅Назад",
                                         callback_data="go_to_start_buttons")
                )
                await message.answer(
                    text=f"👤Reservation ID: {reservation.id}\n"
                    f"🔧Сервис: {reservation.service}\n"
                    f"📆Дата: {reservation.date}\n"
                    f"🕑Время: {reservation.time}\n"
                    f"💸Цена: {reservation.price}$\n", reply_markup=delete_button)

            if await get_language(message.from_user.id) == "en":
                delete_button = InlineKeyboardMarkup()
                delete_button.row(
                    InlineKeyboardButton(text="Delete order",
                                         callback_data=f"delete_reservation{res_id}")
                )
                delete_button.row(
                    InlineKeyboardButton(text="⬅Go back",
                                         callback_data="go_to_start_buttons")
                )
                await message.answer(
                    text=f"👤Reservation ID: {reservation.id}\n"
                    f"🔧Service: {reservation.service}\n"
                    f"📆Date: {reservation.date}\n"
                    f"🕑Time: {reservation.time}\n"
                    f"💸Cost: {reservation.price}$\n", reply_markup=delete_button)

            if await get_language(message.from_user.id) == "uz":
                delete_button = InlineKeyboardMarkup()
                delete_button.row(
                    InlineKeyboardButton(text="Bekor qilish",
                                         callback_data=f"delete_reservation{res_id}")
                )
                delete_button.row(
                    InlineKeyboardButton(text="⬅Orqaga",
                                         callback_data="go_to_start_buttons")
                )
                await message.answer(
                    text=f"👤Reservation ID: {reservation.id}\n"
                    f"🔧Servis: {reservation.service}\n"
                    f"📆Data: {reservation.date}\n"
                    f"🕑Vaqt: {reservation.time}\n"
                    f"💸Narx: {reservation.price}$\n", reply_markup=delete_button)


@dp.callback_query_handler(text_startswith="delete_reservation")
async def delete_users_reservation(callback: types.CallbackQuery):
    await callback.answer()
    text = callback.message.text.split()
    res_id = int(text[2])
    await delete_reservation(res_id)
    if await get_language(callback.from_user.id) == "ru":
        await callback.message.answer("Заказ удален✅", reply_markup=user_start_keyboard)
    if await get_language(callback.from_user.id) == "en":
        await callback.message.answer("Order deleted✅", reply_markup=user_start_keyboard_en)
    if await get_language(callback.from_user.id) == "uz":
        await callback.message.answer("Buyurtma bekor qilindi✅", reply_markup=user_start_keyboard_uz)


@dp.callback_query_handler(text="go_to_start_buttons")
async def go_to_main_menu(callback: types.CallbackQuery):
    await callback.answer()
    if await get_language(callback.from_user.id) == "ru":
        await callback.message.answer("Выберите раздел⬇:", reply_markup=user_start_keyboard)
    if await get_language(callback.from_user.id) == "en":
        await callback.message.answer("Choose⬇:", reply_markup=user_start_keyboard_en)
    if await get_language(callback.from_user.id) == "ru":
        await callback.message.answer("Tanlang⬇:", reply_markup=user_start_keyboard_uz)


@dp.message_handler(text="ℹИнформация")
@dp.message_handler(text="ℹInfo")
@dp.message_handler(text="ℹContact info")
async def get_info(message: types.Message):
    if await get_language(message.from_user.id) == "ru":
        await message.answer(text="Выберите нужный вам раздел⬇", reply_markup=info_keyboard)
    if await get_language(message.from_user.id) == "en":
        await message.answer(text="What do you want⬇", reply_markup=info_keyboard_en)
    if await get_language(message.from_user.id) == "uz":
        await message.answer(text="Tanlang⬇", reply_markup=info_keyboard_uz)


@dp.message_handler(text="💬Оставить отзыв")
@dp.message_handler(text="💬Leave comment")
@dp.message_handler(text="💬Kommentariy qoldirish")
async def leave_comment(message: types.Message):
    if await get_language(message.from_user.id) == "ru":
        await message.answer("Ваш отзыв: ", reply_markup=ReplyKeyboardRemove())
    if await get_language(message.from_user.id) == "en":
        await message.answer("Your review: ", reply_markup=ReplyKeyboardRemove())
    if await get_language(message.from_user.id) == "uz":
        await message.answer("Sizning kommentariyingiz: ", reply_markup=ReplyKeyboardRemove())
    await Review.comment.set()

@dp.message_handler(state=Review.comment)
async def get_comment(message: types.Message, state=FSMContext):
    review_from_user = message.text
    await state.update_data(comment=review_from_user)
    await state.reset_state(with_data=True)

    if await get_language(message.from_user.id) == "ru":
        await message.answer("Спасибо за оставленный отзыв☺", reply_markup=user_start_keyboard)
    if await get_language(message.from_user.id) == "en":
        await message.answer("Thank you for your review☺", reply_markup=user_start_keyboard_en)
    if await get_language(message.from_user.id) == "uz":
        await message.answer("Kommentariyingiz uchun raxmat☺", reply_markup=user_start_keyboard_uz)
    data = await state.get_data()
    dt = datetime.datetime.now()
    date = dt.strftime("%Y/%m/%d")
    await add_comment(
        date=date,
        comment=review_from_user,
        user_id=message.from_user.id
    )

    await bot.send_message(chat_id=admins[0],
        text=f"💬NEW COMMENT\n\n"\
            f"Comment: {review_from_user}\n"
    )


@dp.message_handler(text="☎Контакты")
@dp.message_handler(text="☎Kontaktlar")
@dp.message_handler(text="☎Contacts")
async def get_contacts(message: types.Message):
    if await get_language(message.from_user.id) == "ru":
        await message.answer(text="Для обратной связи\n"\
                         "@autoserviceadmin", reply_markup=user_start_keyboard)
    if await get_language(message.from_user.id) == "en":
        await message.answer(text="Admin: @autoserviceadmin\n"\
                         "☎Tel: +998336943010", reply_markup=user_start_keyboard_en)
    if await get_language(message.from_user.id) == "uz":
        await message.answer(text="Bog'lanish uchun: \n"\
                         "@autoserviceadmin", reply_markup=user_start_keyboard_uz)

@dp.message_handler(text="🏠Главное меню")
@dp.message_handler(text="🏠Main menu")
@dp.message_handler(text="🏠Bosh menu")
async def main_menu(message: types.Message):
    if await get_language(message.from_user.id) == "ru":
        await message.answer("Выберите раздел⬇: ", reply_markup=user_start_keyboard)
    if await get_language(message.from_user.id) == "en":
        await message.answer("Choose what you want⬇: ", reply_markup=user_start_keyboard_en)
    if await get_language(message.from_user.id) == "uz":
        await message.answer("Tanlang⬇: ", reply_markup=user_start_keyboard_uz)


@dp.message_handler(text="🤝Сотрудничество")
@dp.message_handler(text="🤝Cooperation")
@dp.message_handler(text="🤝Hamkorlik")
async def cooperation(message: types.Message):
    if await get_language(message.from_user.id) == "ru":
        await message.answer("Мы рады сотрудничеству с вашей компанией, "\
                             "если это будет полезно для вашей компании, для нас, и конечно для общества\n"\
                             "Для более подробной информации: @autoserviceadmin\n"\
                             "☎Tel: +998336943010",
                             reply_markup=user_start_keyboard)

    if await get_language(message.from_user.id) == "en":
        await message.answer("We are happy to cooperate with you, "\
                             "if it is benefitial for your company, for us and of course, for our society\n"\
                             "To acquire more info: @autoserviceadmin\n"\
                             "☎Tel: +998336943010",
                             reply_markup=user_start_keyboard_en)

    if await get_language(message.from_user.id) == "uz":
        await message.answer("Agarda hamkorlik sizning kompaniyangiz uchun, "\
                             "biz uchun va jamiyat uchun foydali bo'lsa biz hamkorlikga kirishishga tayyormiz\n"\
                             "Ko'proq ma'lumot uchun: @autoserviceadmin\n"\
                             "☎Tel: +998336943010",
                             reply_markup=user_start_keyboard_uz)
