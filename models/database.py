import mysql.connector

class FashionHubDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()

  
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, values=None):
        self.connect()
        self.select_database()
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            # Consume any pending results
            if self.cursor.nextset() is not None:
                for _ in self.cursor.nextset():
                    pass

            self.conn.commit()
        except mysql.connector.Error as e:
            self.conn.rollback()
        finally:
            self.disconnect()

    def fetch_data(self, query, values=None):
        self.connect()
        self.select_database()
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.disconnect()
        return result

    def create_database(self):
        self.connect()
        try:
            query = f"CREATE DATABASE IF NOT EXISTS {self.database}"
            self.cursor.execute(query)
            self.conn.commit()
        except mysql.connector.Error as e:
            self.conn.rollback()
        finally:
            self.disconnect()

    def select_database(self):
        query = f"USE {self.database}"
        self.cursor.execute(query)

    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INT NOT NULL,
            image_url VARCHAR(255) NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );
        """
        self.execute_query(query)

    def drop_tables(self):
        query = "DROP TABLE IF EXISTS products, categories"
        self.execute_query(query)

    def drop_database(self):
        query = f"DROP DATABASE IF EXISTS {self.database}"
        self.execute_query(query)

    def insert_product(self, category_id, name, description, price, stock_quantity, image_url):
        query = "INSERT INTO products (category_id, name, description, price, stock_quantity, image_url) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        values = (category_id, name, description, price, stock_quantity, image_url)
        self.execute_query(query, values)

    def update_product(self, product_id, **columns):
        set_clause = ", ".join(f"{column} = %s" for column in columns.keys())
        query = f"UPDATE products SET {set_clause} WHERE product_id = %s"

        values = list(columns.values())
        values.append(product_id)

        self.execute_query(query, values)


    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE product_id = %s"
        values = (product_id,)
        self.execute_query(query, values)

    def get_products(self):
        query = "SELECT * FROM products"
        return self.fetch_data(query)

    def get_products_by_category_id(self, category_id):
        query = "SELECT * FROM products WHERE category_id = %s"
        values = (category_id,)
        return self.fetch_data(query, values)

    def insert_category(self, name):
        query = "INSERT INTO categories (name) VALUES (%s)"
        values = (name,)
        self.execute_query(query, values)

    def update_category(self, category_id, name):
        query = "UPDATE categories SET name = %s WHERE category_id = %s"
        values = (name, category_id)
        self.execute_query(query, values)

    def delete_category(self, category_id):
        query = "DELETE FROM categories WHERE category_id = %s"
        values = (category_id,)
        self.execute_query(query, values)

    def get_categories(self):
        query = "SELECT * FROM categories"
        return self.fetch_data(query)

    def update_column(self, table, primary_key_column, primary_key_value, column_name, new_value):
        query = f"UPDATE {table} SET {column_name} = %s WHERE {primary_key_column} = %s"
        values = (new_value, primary_key_value)
        self.execute_query(query, values)
