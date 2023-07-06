import os
from dotenv import load_dotenv
from models.database import FashionHubDatabase
from models.products_info import products

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')

# Create an instance of FashionHubDatabase
db = FashionHubDatabase(host=db_host, user=db_user, password=db_password, database=db_database)

def initDatabase():
    # Create the database
    db.create_database()
    # Create the tables
    db.create_tables()
    # Add categories
    categories = ['Women Formal', 'Women Casual', 'Men Formal', 'Men Casual', 'Accessories']
    for category in categories:
        db.insert_category(category)

def storeProductsMysql():
    # Save to database
    for product in products:
        db.insert_product(
            category_id=product['category_id'],
            name=product['name'],
            description=product['description'],
            price=product['price'],
            stock_quantity=product['stock_quantity'],
            image_url=product['image_url']
    )

def get_products():
    product_list = []
    saved_products = db.get_products()
    for product in saved_products:
        reconstructed_product = {
            'product_id': product[0],
            'category_id': product[1],
            'name': product[2],
            'description': product[3],
            'price': float(product[4]),
            'stock_quantity': product[5],
            'image_url': product[6]
        }
        product_list.append(reconstructed_product)
    return product_list

def get_products_by_category_id(category_id):
      product_list = []
      saved_products = db.get_products_by_category_id(category_id)
      for product in saved_products:
          reconstructed_product = {
              'product_id': product[0],
              'category_id': product[1],
              'name': product[2],
              'description': product[3],
              'price': float(product[4]),
              'stock_quantity': product[5],
              'image_url': product[6]
          }
          product_list.append(reconstructed_product)
      return product_list

def get_categories():
    category_list = []
    saved_categories = db.get_categories()
    for category in saved_categories:
        category_list.append(category[1])
    return category_list

def search_products(search_word, products):
    matching_products = []

    for product in products:
        if search_word.lower() in product['name'].lower():
            matching_products.append(product)

    return matching_products

def clear_database():
    db.drop_tables()

#initDatabase()
#storeProductsMysql()
#print(get_categories())
#clear_database()
#search_products('crochet', get_products())
