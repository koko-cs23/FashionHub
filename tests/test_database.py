import unittest
import models
from models.database import FashionHubDatabase


class FashionHubDatabaseTests(unittest.TestCase):

    def setUp(self):
        # Create an instance of FashionHubDatabase
        self.db = FashionHubDatabase(host='localhost', user='root', password='root', database='fashionhub')
        # Create database
        self.db.create_database()
        # Create tables
        self.db.create_tables()

    def tearDown(self):
        # Drop the tables and database after each test
        self.db.drop_tables()
        self.db.drop_database()

    def test_insert_category(self):
        # Test inserting a category
        self.db.insert_category('Category 2')
        # Fetch the inserted category from the database and assert its existence
        categories = self.db.get_categories()
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0][1], 'Category 2')

    def test_insert_product(self):
        # Test inserting a product
        self.db.insert_category('Category 1')
        self.db.insert_product(category_id=1, name="Men's T-Shirt", description="Classic black t-shirt for men",
                               price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image1.jpg')
        # Fetch the inserted product from the database and assert its existence
        products = self.db.get_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][2], "Men's T-Shirt")

    def test_update_category(self):
        # Test updating a category
        self.db.insert_category('Category 1')
        self.db.update_category(category_id=1, name='Ferrari')
        # Fetch the updated category from the database and assert the name change
        categories = self.db.get_categories()
        self.assertEqual(categories[0][1], 'Ferrari')

    def test_update_product(self):
        # Test updating a product
        self.db.insert_category('Category 1')
        self.db.insert_product(category_id=1, name="Men's T-Shirt", description="Classic black t-shirt for men",
                               price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image1.jpg')
        self.db.update_product(product_id=1, category_id=1, name="Men's New T-Shirt", description="Stylish black t-shirt for men",
                               price=24.99, stock_quantity=40, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image2.jpg')
        # Fetch the updated product from the database and assert the changes
        products = self.db.get_products()
        self.assertEqual(products[0][2], "Men's New T-Shirt")
        self.assertEqual(products[0][5], 40)

    def test_update_column(self):
        # Test updating a column
        self.db.insert_category('Category 1')
        self.db.update_column("categories", "category_id", 1, "name", "Volvo")
        # Fetch the updated category from the database and assert the name change
        categories = self.db.get_categories()
        self.assertEqual(categories[0][1], 'Volvo')

    def test_delete_product(self):
        # Test deleting a product
        self.db.insert_category('Category 1')
        self.db.insert_product(category_id=1, name="Men's T-Shirt", description="Classic black t-shirt for men",
                               price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image1.jpg')
        self.db.delete_product(product_id=1)
        # Fetch the deleted product from the database and assert its non-existence
        products = self.db.get_products()
        self.assertEqual(len(products), 0)

    def test_delete_category(self):
        # Test deleting a category
        self.db.insert_category('Category 1')
        self.db.delete_category(category_id=1)
        categories = self.db.get_categories()
        self.assertEqual(len(categories), 0)

    def test_get_categories(self):
        # Test fetching all categories
        self.db.insert_category('Category 1')
        self.db.insert_category('Category 2')
        categories = self.db.get_categories()
        # Assert the expected number of categories and their content
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0][1], 'Category 1')
        self.assertEqual(categories[1][1], 'Category 2')

    def test_get_products(self):
        # Test fetching all products
        self.db.insert_category('Category 1')
        self.db.insert_category('Category 2')
        self.db.insert_product(category_id=1, name="Men's T-Shirt", description="Classic black t-shirt for men",
                               price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image1.jpg')
        self.db.insert_product(category_id=2, name="Women's T-Shirt", description="Classic black t-shirt for women",
                               price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image2.jpg')
        products = self.db.get_products()
        # Assert the expected number of products and their content
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0][2], "Men's T-Shirt")
        self.assertEqual(products[1][2], "Women's T-Shirt")

    def test_get_products_by_category_id(self):
        # Insert test data into the database
        self.db.insert_category('Category 1')
        self.db.insert_category('Category 2')
        self.db.insert_product(category_id=1, name="Men's T-Shirt", description="Classic black t-shirt for men",
                           price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image1.jpg')
        self.db.insert_product(category_id=2, name="Women's T-Shirt", description="Classic black t-shirt for women",
                           price=19.99, stock_quantity=50, image_url='https://ucarecdn.com/d588d187-585b-4be1-b1cf-6c0af9c19295/image2.jpg')

        # Call the function being tested
        category_id = 1
        products = self.db.get_products_by_category_id(category_id)

        # Assert the expected number of products and their content
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][2], "Men's T-Shirt")

        # Call the function being tested with a different category_id
        category_id = 2
        products = self.db.get_products_by_category_id(category_id)

        # Assert the expected number of products and their content
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][2], "Women's T-Shirt")

if __name__ == '__main__':
    unittest.main()
