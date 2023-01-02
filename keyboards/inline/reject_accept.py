from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

accept_reject = InlineKeyboardMarkup(row_width=1)
accept_reject.row(
    InlineKeyboardButton(
        text="Принять☑", callback_data="accept_order"))

accept_reject.row(
    InlineKeyboardButton(
        text="Отменить✖", callback_data="reject_order"
    ))

accept_reject_en = InlineKeyboardMarkup(row_width=1)
accept_reject_en.row(
    InlineKeyboardButton(
        text="Accept☑", callback_data="accept_order"))

accept_reject_en.row(
    InlineKeyboardButton(
        text="Reject✖", callback_data="reject_order"
    ))

accept_reject_uz = InlineKeyboardMarkup(row_width=1)
accept_reject_uz.row(
    InlineKeyboardButton(
        text="Qabul qilish☑", callback_data="accept_order"))

accept_reject_uz.row(
    InlineKeyboardButton(
        text="Rad etish✖", callback_data="reject_order"
    ))
