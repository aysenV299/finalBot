import sqlite3

class DatabaseMethods:
  def __init__(self):
        self.database = sqlite3.connect('models/storage.db')
        self.cursor = self.database.cursor()

  def create_products_table(self) -> None:
    self.cursor.execute("CREATE TABLE IF NOT EXISTS products("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "type TEXT, "
                "name TEXT, "
                "description TEXT, "
                "price INTEGER, "
                "photo_unique_id TEXT, "
                "photo_id TEXT)")
    self.cursor.execute("CREATE TABLE IF NOT EXISTS cart("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id TEXT, "
                "type TEXT, "
                "name TEXT, "
                "price INTEGER)")
    self.database.commit()
  
  def insert_product(self, item_data) -> None:
    query = "INSERT INTO products (type, name, description, price, photo_unique_id, photo_id) " \
            "VALUES (:type, :name, :description, :price, :photo_unique_id, :photo_id)"
    self.cursor.execute(query, {
        'type': item_data['type'],
        'name': item_data['name'],
        'description': item_data['description'],
        'price': item_data['price'],
        'photo_unique_id': item_data['photo_unique_id'],
        'photo_id': item_data['photo_id']
    })
    self.database.commit()

  def check_product_exists(self, name: str) -> bool:
    query = "SELECT id FROM products WHERE name = :name"
    self.cursor.execute(query, {'name': name})
    response = self.cursor.fetchone()
    if response:
        return True
    else:
        return False
  
  def remove_product(self, name: str) -> None:
    query  = "DELETE FROM products WHERE name = :name"
    self.cursor.execute(query, {'name': name})
    self.database.commit()

  def get_all_products(self):
    query = "SELECT * FROM products"
    self.cursor.execute(query)
    response = self.cursor.fetchall()
    return response
  
  def show_product(self, name: str):
    query = "SELECT * FROM products WHERE name = :name"
    self.cursor.execute(query, {'name': name})
    response = self.cursor.fetchone()
    return response
  
  def add_to_cart(self, item_data, user_id: str) -> None:
    query = "INSERT INTO cart (user_id, type, name, price) " \
            "VALUES (:user_id, :type, :name, :price)"
    self.cursor.execute(query, {
        'user_id': user_id,
        'type': item_data[1],
        'name': item_data[2],
        'price': item_data[4],
    })
    self.database.commit()

  def get_cart(self, user_id: str) -> list:
    query = "SELECT type, name, price FROM cart WHERE user_id = :user_id"
    self.cursor.execute(query, {'user_id': user_id})
    response = self.cursor.fetchall()
    return response

  def clear_cart(self, user_id: str) -> list:
    query  = "DELETE FROM cart WHERE user_id = :user_id"
    self.cursor.execute(query, {'user_id': user_id})
    self.database.commit()

