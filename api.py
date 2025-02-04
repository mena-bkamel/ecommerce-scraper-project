from flask import Flask, jsonify

app = Flask(__name__)

SCRAPED_DATA = ...


@app.route('/sites', methods=['GET'])
def list_sites():
    return jsonify({"supported_sites": ["Amazon", "eBay", "Target"]})


@app.route('/compare/<product_name>', methods=['GET'])
def compare_product(product_name):
    product_name = product_name.title()
    if product_name in SCRAPED_DATA:
        return jsonify(SCRAPED_DATA[product_name])
    return jsonify({"error": "Product not found"}), 404
