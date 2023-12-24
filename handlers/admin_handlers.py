from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from filters.filters import IsAdmin, ExistProduct
from keyboards.reply_keyboards import admin_action_kb, cancel_kb, admin_kb
from keyboards.inline_keyboards import products_kb
from states import AddProductFSM, RemoveProductFSM
from aiogram.fsm.context import FSMContext
from lexicon import TYPE_BUTTONS

router = Router()

@router.message((F.text == "Панель управления 💻"), StateFilter(default_state), IsAdmin())
async def process_panel_command(message: Message):
    await message.answer(text="Выберете функцию 🛠", reply_markup=admin_action_kb)

@router.message(F.text == "Отмена ❌", StateFilter(default_state), IsAdmin())
@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text="Вы не заполняете форму ❌", reply_markup=admin_kb)

@router.message(F.text == "Отмена ❌", ~StateFilter(default_state), IsAdmin())
@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text="Вы отменили заполнение формы ✅", reply_markup=admin_kb)
    await state.clear()
    
@router.message(F.text == "Добавление товара 🟢", StateFilter(default_state), IsAdmin())
async def process_add_product(message: Message, state: FSMContext):
        await message.answer(text="Тип товара 👜", reply_markup=products_kb)
        await state.set_state(AddProductFSM.type_order)

@router.callback_query(StateFilter(AddProductFSM.type_order), F.data.in_(["clothes", "sneakers", "accessories"]), IsAdmin())
async def process_type_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type=TYPE_BUTTONS[callback.data])
    await callback.message.delete()
    await callback.message.answer(text="Введите название товара 🖍", reply_markup=cancel_kb)
    await state.set_state(AddProductFSM.name_order)

@router.message(StateFilter(AddProductFSM.type_order), IsAdmin())
async def incorrect_type(message: Message):
    await message.answer(text="Выберете тип товара ❌", reply_markup=cancel_kb)

@router.message(StateFilter(AddProductFSM.name_order), IsAdmin(), lambda x: len(f'product:{x.text}'.encode()) <= 64)
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Введите описание товара 🖍", reply_markup=cancel_kb)
    await state.set_state(AddProductFSM.description_order)

@router.message(StateFilter(AddProductFSM.name_order), IsAdmin())
async def incorrect_name(message: Message):
    await message.answer(text="Вы ввели неверное название ❌", reply_markup=cancel_kb)

@router.message(StateFilter(AddProductFSM.description_order), lambda x: 1 <= len(x.text) <= 250, IsAdmin())
async def process_descr_sent(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text="Введите цену на товар 🖍", reply_markup=cancel_kb)
    await state.set_state(AddProductFSM.price_order)

@router.message(StateFilter(AddProductFSM.description_order), IsAdmin())
async def incorrect_descr(message: Message):
    await message.answer(text="Введите корректное описание товара. Оно должно быть не более 250 символов ❌", reply_markup=cancel_kb)

@router.message(StateFilter(AddProductFSM.price_order), lambda x: x.text.isdigit(), IsAdmin())
async def process_price_sent(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer(text="Загрузите фотографию на товар 📷", reply_markup=cancel_kb)
    await state.set_state(AddProductFSM.photo_order)

@router.message(StateFilter(AddProductFSM.price_order), IsAdmin())
async def incorrect_price(message: Message):
    await message.answer(text="Неверно введена цена ❌", reply_markup=cancel_kb)

@router.message(StateFilter(AddProductFSM.photo_order), F.photo[-1].as_("largest_photo"), IsAdmin())
async def process_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize, database):
    try:
        await state.update_data(
            photo_unique_id=largest_photo.file_unique_id,
            photo_id=largest_photo.file_id,
        )

        response = await state.get_data()
        database.insert_product(response)

        await state.clear()
        await message.answer(text="Товар успешно добавлен ✅", reply_markup=admin_kb)
    except:
        await message.answer(text="Произошла ошибка при добавлении товара ❌", reply_markup=admin_kb)
        await state.clear()


@router.message(StateFilter(AddProductFSM.photo_order), IsAdmin())
async def incorrect_photo(message: Message):
    await message.answer(text="Некорректное изображение ❌", reply_markup=cancel_kb)

@router.message(F.text == "Удаление товара 🔴", StateFilter(default_state), IsAdmin())
async def process_remove_product(message: Message, state: FSMContext):
        await message.answer(text="Введите название товара для удаления 🖍", reply_markup=cancel_kb)
        await state.set_state(RemoveProductFSM.name_order)

@router.message(StateFilter(RemoveProductFSM.name_order), IsAdmin(), ExistProduct())
async def correct_product(message: Message, state: FSMContext, database):
    name = message.text
    try:
        database.remove_product(name)
        await message.answer(text="Товар успешно удален ✅", reply_markup=admin_kb)
        await state.clear()
    except:
        await message.answer(text="Ошибка при удаление товара ❌", reply_markup=admin_kb)
        await state.clear()

@router.message(StateFilter(RemoveProductFSM.name_order), IsAdmin())
async def incorrect_product(message: Message):
    await message.answer(text="Товара с таким названием не существует в каталоге ❌")
