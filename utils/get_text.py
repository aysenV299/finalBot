def get_caption(product: dict) -> str:
    return f'<b>Описание товара</b> 🗂:\
    \n├ <b>Тип товара: </b> <code>{product[1]}</code>\
    \n├ <b>Название: </b> <code>{product[2]}</code>\
    \n├ <b>Описание: </b> <code>{product[3]}</code>\
    \n└ <b>Цена: </b> <code>{product[4]} рублей</code>'

def get_cart(product: list, message, total_price: str) -> str:
    # username = message.from_user.username
    # user_id = message.from_user.id
    # first_name = message.from_user.first_name
    # last_name = message.from_user.last_name

    cart_text = '<b>Корзина</b> 🛒\n\n'

    for product in product:
        cart_text += f'├ {product[1]}\n'
        cart_text += f'├ <b>Цена</b>: <code>{product[2]} рублей</code>\n'
        cart_text += f'├─────────────────\n'
    
    cart_text += f'<b>└ Итоговая цена:</b> <code>{total_price} рублей</code>'
    return cart_text

def get_order(cart, message, user_data) -> str:
    username = message.from_user.username
    user_id = message.from_user.id
    contact_data = user_data['contact']
    user_name = user_data['name']
    total_price = 0

    for item in cart:
        total_price += item[2]
    
    order_text = f'<b>Заказ от {user_id}</b> 🛒\n\n'



    for product in cart:
        order_text += f'├ {product[1]}\n'
        order_text += f'├ <b>Цена</b>: <code>{product[2]} рублей</code>\n'
        order_text += f'├─────────────────\n'
    
    order_text += f'<b>├ Итоговая цена:</b> <code>{total_price} рублей</code>\n'
    order_text += f'├─────────────────\n'
    order_text += f'<b>├ Покупатель 👤</b>\n'
    order_text += f'│\n'
    order_text += f'<b>├ Telegam:</b> @{username}\n'
    order_text += f'<b>├ ID:</b> <code>{user_id}</code>\n'
    order_text += f'<b>├ Контакты:</b> <code>{contact_data}</code>\n'
    order_text += f'<b>└ Имя:</b> <code>{user_name}</code>\n'
    return order_text

