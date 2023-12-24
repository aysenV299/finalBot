from aiogram.filters.callback_data import CallbackData

class ProductsCallbackFactory(CallbackData, prefix="product"):
  product_name: str

class AddProductsCallbackFactory(CallbackData, prefix="add"):
  product_name: str
