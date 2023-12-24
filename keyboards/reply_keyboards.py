from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main_kb_builder = ReplyKeyboardBuilder()

main_btns: list[KeyboardButton] = [
    KeyboardButton(text="Каталог 🗂"),
    KeyboardButton(text="Корзина 🛒"),
    KeyboardButton(text="Контакты 🗣"),
]

main_kb_builder.row(*main_btns, width=2)

main_kb = main_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберете действие...",
)


admin_kb_builder = ReplyKeyboardBuilder()

admin_btns: list[KeyboardButton] = [
    KeyboardButton(text="Каталог 🗂"),
    KeyboardButton(text="Корзина 🛒"),
    KeyboardButton(text="Контакты 🗣"),
    KeyboardButton(text="Панель управления 💻"),
]

admin_kb_builder.row(*admin_btns, width=2)

admin_kb = admin_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберете действие...",
)


admin_action_kb_builder = ReplyKeyboardBuilder()

admin_action_btns: list[KeyboardButton] = [
    KeyboardButton(text="Добавление товара 🟢"),
    KeyboardButton(text="Удаление товара 🔴"),
]

admin_action_kb_builder.row(*admin_action_btns, width=2)

admin_action_kb = admin_action_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберете действие...",
)


cancel_kb_builder = ReplyKeyboardBuilder()

cancel_kb_builder.row(KeyboardButton(text="Отмена ❌"), width=1)

cancel_kb = cancel_kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
