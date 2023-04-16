from flask import Flask, request
from src.api.entities.product import create_product, get_product, delete_product, list_all_product, update_product
from src.api.entities.insert_media import create_midia

app = Flask(__name__)


@app.route("/")
def hello_nina():
    return "Hello, Nina!!"

@app.route("/product", methods=["POST"])
def create_product_route():
    payload = request.get_json()
    return create_product(payload)

	
@app.route("/product/<string:product_id>", methods=['GET'])
def get_product_route(product_id):
    return get_product(product_id)

@app.route("/product/delete/<string:product_id>", methods=['DELETE'])
def delete_product_route(product_id):
    return delete_product(product_id)

@app.route("/products/list", methods=['GET'])
def list_all_product_route():
    return list_all_product()

@app.route("/product/update/<string:product_id>", methods=['PUT'])
def update_product_route(product_id):
    update_data = request.get_json()
    return update_product(product_id, update_data)

@app.route("/midia", methods=['POST'])
def create_midia_route():
    payload = request.get_json()
    return payload

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
