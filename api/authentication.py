from flask import Blueprint, jsonify, request

# Create a blueprint
auth_blueprint = Blueprint('api', __name__)

# Define routes under the blueprint
@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    return jsonify({"message": "Hello, World!"})

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return jsonify({"message": f"Hello login"})

