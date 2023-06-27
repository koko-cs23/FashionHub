from flask import Flask, render_template
#from upload_care import get_uploaded_image_urls
from products_info import products

app = Flask(__name__)

# Function to retrieve a product based on the given product ID
def get_product(product_id):
    for product in products:
        if product['product_id'] == product_id:
            return product
    return None

@app.route('/')
def home():
    #image_urls = get_uploaded_image_urls()

    return render_template('index.html', products=products)

@app.route('/filter_search')
def filter_search():
    return render_template('filter_search.html')

@app.route('/product/<int:product_id>')
def product(product_id):
    product = get_product(product_id)
    if product:
        return render_template('product.html', product=product)
    else:
        return "Product not found."

if __name__ == '__main__':
    app.run()
