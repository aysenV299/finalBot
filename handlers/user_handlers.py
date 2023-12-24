from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from keyboards.reply_keyboards import main_kb, admin_kb, cancel_kb
from keyboards.inline_keyboards import create_products_keyboard, show_product_keyboard, cart_keyboard, links_keyboard
from lexicon.commands import LEXICON_COMMANDS
from keyboards.callbackFactory import ProductsCallbackFactory, AddProductsCallbackFactory
from utils import get_caption, get_cart, get_order
from states import MakeOrderFSM

router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, configuration):
    start_text = f"Привет, {message.from_user.username} ❤️\nРады приветствовать тебя в нашем мультибрендовом магазине 🔥!  Здесь тебя ждут стильные вещи от лучших брендов 🛍️. Приглашаем оставаться с нами и быть в курсе последних новинок ✨! "
    if message.from_user.id in configuration.tg_bot.admin_ids:
        await message.answer(text=start_text, reply_markup=admin_kb)
    else:
        await message.answer(text=start_text, reply_markup=main_kb)

@router.message(Command(commands="help"), StateFilter(default_state))
async def process_help_command(message: Message, configuration):
    help = "🤖 <b>Команды доступные в боте</b>\n\n"
    for key, value in LEXICON_COMMANDS.items():
        help += f"➖ {key} - {value}\n"

    if message.from_user.id in configuration.tg_bot.admin_ids:
        await message.answer(text=help, reply_markup=admin_kb)
    else:
        await message.answer(text=help, reply_markup=main_kb)


@router.message((F.text == "Каталог 🗂"), StateFilter(default_state))
async def process_panel_command(message: Message, database):
    try:
        response = database.get_all_products()
        products_keyboard = create_products_keyboard(response, 1)
        
        await message.answer(text="Каталог 🛍", reply_markup=products_keyboard)
    except:
        await message.answer(text="Ошибка при вызове каталога ❌", reply_markup=main_kb)


@router.callback_query(ProductsCallbackFactory.filter(), StateFilter(default_state))
async def process_category_press(callback: CallbackQuery, callback_data: ProductsCallbackFactory, database):
    product_name = callback_data.product_name
    
    try:
        response = database.show_product(product_name)
        caption = get_caption(response)

        keyboard = show_product_keyboard(response[2], 1)
        await callback.message.answer_photo(
            photo=response[6],
            caption=caption,
            reply_markup=keyboard,
        )

        await callback.message.delete()
        await callback.answer()
    except:
        await callback.message.answer(text="Ошибка при вызове товара ❌", reply_markup=main_kb)

@router.callback_query(F.data == "back_btn", StateFilter(default_state))
async def back_btn_command(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Вы перемещены в меню 🔔", reply_markup=main_kb)
    await callback.answer()

@router.callback_query(F.data == "back_to_products_btn", StateFilter(default_state))
async def back_to_products_btn_command(callback: CallbackQuery, database):
    try:
        response = database.get_all_products()
        products_keyboard = create_products_keyboard(response, 1)
        
        await callback.message.answer(text="<b>Каталог</b> 🛍", reply_markup=products_keyboard)

        await callback.message.delete()
        await callback.answer()
    except:
        await callback.message.answer(text="Ошибка при вызове списка товаров ❌", reply_markup=main_kb)

@router.callback_query(AddProductsCallbackFactory.filter(), StateFilter(default_state))
async def add_to_cart_press(callback: CallbackQuery, callback_data: ProductsCallbackFactory, database):
    product_name = callback_data.product_name
    user_id = callback.message.chat.id
    try:
        response = database.show_product(product_name)
        database.add_to_cart(response, str(user_id))
        await callback.message.answer_sticker(r'CAACAgIAAxkBAAEoaeRlh49v7tzgcrgszl8qS_ikPiZlEwACUDkAAulVBRg9Q_7QMuwdwDME')
        await callback.message.answer(text="Вы добавили товар в корзину ✅", reply_markup=main_kb)
        await callback.message.delete()
        await callback.answer()
    except:
        await callback.message.answer(text="Ошибка при добавлении товара в корзину ❌", reply_markup=main_kb)

@router.message((F.text == "Корзина 🛒"), StateFilter(default_state))
async def process_cart_command(message: Message, database):
    user_id = message.from_user.id

    try:
        cart = database.get_cart(user_id)
        total_price = 0

        if not cart:
            await message.answer(text="Корзина пустая 🔔", reply_markup=main_kb)
            return
        
        for item in cart:
            total_price += item[2]

        keyboard = cart_keyboard()

        cart_text = get_cart(cart, message, str(total_price))
        await message.answer(text=cart_text, reply_markup=keyboard)
    except:
        await message.answer(text="Ошибка при вызове корзины ❌", reply_markup=main_kb)

@router.callback_query(F.data == "clear_cart", StateFilter(default_state))
async def clear_cart_command(callback: CallbackQuery, database):
    try:
        user_id = callback.message.chat.id
        database.clear_cart(user_id)
        await callback.message.answer(text="Корзина очищена ✅", reply_markup=main_kb)
        await callback.message.delete()
        await callback.answer()
    except:
        await callback.message.answer(text="Ошибка при очистке корзины ❌", reply_markup=main_kb)

@router.message(F.text == "Отмена ❌", StateFilter(default_state))
@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text="Вы не заполняете форму ❌", reply_markup=main_kb)

@router.message(F.text == "Отмена ❌", ~StateFilter(default_state))
@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text="Вы отменили заполнение формы ✅", reply_markup=main_kb)
    await state.clear()

@router.callback_query(F.data == "make_order", StateFilter(default_state))
async def make_order_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите данные для связи 🖍", reply_markup=cancel_kb)
    await callback.message.delete()
    await callback.answer()
    await state.set_state(MakeOrderFSM.contact_order)

@router.message(StateFilter(MakeOrderFSM.contact_order))
async def send_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer(text="Введите наше имя 🖍", reply_markup=cancel_kb)
    await state.set_state(MakeOrderFSM.name_order)

@router.message(StateFilter(MakeOrderFSM.name_order))
async def send_contact(message: Message, state: FSMContext, database, configuration, bot):
    try:
        group_id = configuration.group.ID
        await state.update_data(name=message.text)
        user_id = message.from_user.id
        user_data = await state.get_data()

        await state.clear()

        cart = database.get_cart(user_id)

        order_text = get_order(cart, message, user_data)

        await bot.send_message(group_id, order_text)
        database.clear_cart(user_id)
        await message.answer_sticker(r'CAACAgIAAxkBAAEoaeJlh47tEp8C6p_ZaBVQrHPUdGTvxgACVDkAAulVBRjtsQxMrEp47DME')
        await message.answer(text="Заказ успешно отправлен ✅", reply_markup=main_kb)
    except:
        await message.answer(text="Ошибка при отправке заказа ❌", reply_markup=main_kb)

@router.message((F.text == "Контакты 🗣"), StateFilter(default_state))
async def process_cart_command(message: Message):
    keyboard = links_keyboard()
    await message.answer(text="<b>Контакты ✉️</b>", reply_markup=keyboard)  