from flask import Blueprint, jsonify, request
from .mongo_connect import DB
import bcrypt
import datetime
import jwt
from dotenv import dotenv_values

config = dotenv_values(".env")

# Create a blueprint
auth_blueprint = Blueprint('api', __name__)

#Function for encoding passwords
def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

#Function for comparing Passwords
def compare_passwords(password, hashed_password):
    print(hashed_password)
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False

#Function for generating token
def generate_token(payload):
    secret = config.get("TOKEN_SECRET")
    return jwt.encode(payload, secret, algorithm="HS256")

# Define routes under the blueprint
@auth_blueprint.route('/signup/buyer', methods=['POST'])
def signup_buyer():
    seller_table = DB['Buyer']
    try:
        required = ['email','name','password','phone_num', 'address']
        user_data = request.get_json()
        for i in required:
            if not i in user_data:
                return jsonify({"message": f"{i} field is missing"})
            
        if seller_table.find_one(filter={"email":user_data["email"]}):
            return jsonify({"status": "This email already exists"})
        
        resp = seller_table.insert_one({
        'email': user_data["email"],
        'name': user_data["name"],
        'password': encrypt_password(user_data["password"]),
        'phone_num': user_data["phone_num"],
        'address': user_data["address"],
        }) 
        return jsonify({"status": f"User added"})
    except Exception as e:
        return jsonify({"error": str(e)})

@auth_blueprint.route('login/buyer', methods=['POST'])
def login_buyer():
    seller_table = DB['Buyer']
    try:
        required = ['email','password']
        user_data = request.get_json()
        for i in required:
            if not i in user_data:
                return jsonify({"message": f"{i} field is missing"})
        info = seller_table.find_one({"email":user_data["email"]},{"password":1})
        if not info:
            return jsonify({"message": "No such account exists"})
        #print(info)
        auth = compare_passwords(user_data["password"],info["password"])
        if auth:
            payload = {
                'email': user_data["email"],
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1000)
            }
            token = generate_token(payload)
            return jsonify({"status": token})
        else:
            return jsonify({"status": "Please enter correct password"})

    except Exception as e:
        return jsonify({"error": str(e)})

