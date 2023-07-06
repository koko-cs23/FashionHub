from flask import Flask, render_template, jsonify, request, make_response
from models.product_manager import get_products, get_categories, get_products_by_category_id, search_products
from services.send_email import sendCustomerInvoice
import time

app = Flask(__name__)

# Get products
products = get_products()
categories = get_categories()

# Function to retrieve a product based on the given product ID
def get_product(product_id):
    for product in products:
        if product['product_id'] == product_id:
            return product
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        keyword = request.form.get('keyword')

        # Perform search based on the keyword (Replace with your actual search logic)
        matching_products = search_products(keyword, products)

        return render_template('index.html', products=matching_products, categories=categories)

    # Render the home template with initial data
    return render_template('index.html', products=products, categories=categories)

@app.route('/product/<int:product_id>',  methods=['GET', 'POST'])
def product(product_id):
    product = get_product(product_id)
    if product:
        return render_template('product.html', product=product)
    else:
        return "Product not found."

@app.route('/purchase/<int:product_id>', methods=['GET', 'POST'])
def purchase(product_id):
    product = get_product(product_id)
    if product:
        return render_template('payment.html', product=product)
    else:
        return "Product not found."

@app.route('/check_payment', methods=['POST'])
def check_payment():
    payment_data = request.get_json()
    # Extract payment details from the JSON payload
    product_id = payment_data.get('product_id')
    card_number = payment_data.get('card_number')
    cvv = payment_data.get('cvv')
    expiry = payment_data.get('expiry')
    amount = payment_data.get('amount')
    email = payment_data.get('email')

    success = sendCustomerInvoice(payment_data, get_product(product_id))

    return jsonify({"success": success})
  # Timestamp helper function
@app.context_processor
def utility_processor():
    def timestamp():
        return str(int(time.time()))
    return dict(timestamp=timestamp)

@app.route('/filter', methods=['POST'])
def filter():
    category_name = request.json.get('category') # Get the category name from the request
    category_id = categories.index(category_name)
    # Get products associated with the category id
    category_products = get_products_by_category_id(category_id + 1)

    # Return the filtered products as a JSON response
    return jsonify(category_products)



if __name__ == '__main__':
    app.run()
