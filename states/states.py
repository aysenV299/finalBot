from aiogram.fsm.state import State, StatesGroup


class AddProductFSM(StatesGroup):
    type_order = State()
    name_order = State()
    description_order = State()
    price_order = State()
    photo_order = State()

class RemoveProductFSM(StatesGroup):
    name_order = State()

class MakeOrderFSM(StatesGroup):
    contact_order = State()
    name_order = State()
