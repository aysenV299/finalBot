
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import TYPE_BUTTONS, LINKS_BUTTONS
from keyboards.callbackFactory import ProductsCallbackFactory, AddProductsCallbackFactory

products_buttons = []

for key, value in TYPE_BUTTONS.items():
    products_buttons.append([InlineKeyboardButton(text=value, callback_data=key)])

products_kb = InlineKeyboardMarkup(inline_keyboard=products_buttons)

def create_products_keyboard(products_list: list, width: int) -> InlineKeyboardMarkup:
    products_kb_builder = InlineKeyboardBuilder()
    
    buttons: list[InlineKeyboardButton] = []
    for product in products_list:
        callback_data = ProductsCallbackFactory(
            product_type=product[1],
            product_name=product[2]
        ).pack()
        text = f"{product[2]} - {product[1]}"

        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=callback_data,
            )
        )
    
    buttons.append(
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data="back_btn",
            )
        )
    
    products_kb_builder.row(*buttons, width=width)

    return products_kb_builder.as_markup()


def show_product_keyboard(product_type: str, width: int) -> InlineKeyboardMarkup:
    products_kb_builder = InlineKeyboardBuilder()
    
    buttons: list[InlineKeyboardButton] = []

    buttons.append(
        InlineKeyboardButton(
            text="Добавить в корзину 🛍",
            callback_data=AddProductsCallbackFactory(
                product_name=product_type
            ).pack()
        )
    )
    
    buttons.append(
            InlineKeyboardButton(
                text="Назад ◀️",
                callback_data="back_to_products_btn",
            )
        )
    
    products_kb_builder.row(*buttons, width=width)

    return products_kb_builder.as_markup()

def cart_keyboard() -> InlineKeyboardMarkup:
    cart_kb_builder = InlineKeyboardBuilder()
    
    buttons: list[InlineKeyboardButton] = []

    buttons.append(
        InlineKeyboardButton(
            text="Сделать заказ ✏️",
            callback_data="make_order"
        )
    )

    buttons.append(
        InlineKeyboardButton(
            text="Очистить корзину 🛒",
            callback_data="clear_cart"
        )
    )
    
    buttons.append(
            InlineKeyboardButton(
                text="Назад ◀️",
                callback_data="back_btn",
            )
        )
    
    cart_kb_builder.row(*buttons, width=2)

    return cart_kb_builder.as_markup()

def links_keyboard() -> InlineKeyboardMarkup:
    links_kb_builder = InlineKeyboardBuilder()
    
    buttons: list[InlineKeyboardButton] = []

    buttons.append(
        InlineKeyboardButton(
            text = 'Менеджер',
            url='https://t.me/curlon'
        )
    )

    buttons.append(
        InlineKeyboardButton(
            text = 'Инстаграм',
            url='https://www.instagram.com/ootd.stoore/'
        )
    )
    
    buttons.append(
            InlineKeyboardButton(
                text="Назад ◀️",
                callback_data="back_btn",
            )
        )
    
    links_kb_builder.row(*buttons, width=2)

    return links_kb_builder.as_markup()

