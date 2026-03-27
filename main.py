from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from functools import wraps
from mongo_model import *
from bson import json_util
import json
import datetime
import jwt
import string
import random # define the random module 

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12))
CORS(app, support_credentials=True)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=get_login(data["user_email"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["name"]:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated


def verify_login(user_id, user, password, account):
    credentials = get_credentials(user_id)
    result = ""
    know_user = credentials

    if know_user == None:
        result = "User not found"
        return result  
    
    if know_user["name"] != user:
        result = "Unknow user"
        return result    
    
    if know_user["password"] != password:
        result = "Denied"
        return result

    if account not in know_user["accounts"]:
        result = "Account not found"
        return result

    result = "Access garantee" 
    return result

@app.route('/login', methods=['POST'])
def auth():
    input_data = request.json
    result = get_login(input_data["email"])

    if result == None:
        return make_response(
            jsonify(
		message='User not found'
            ), 401
        )

    if result["password"] != input_data["password"]:
        return make_response(
            jsonify(
		message='Invalid Login'
            ), 401
        )
    token=jwt.encode({'username': result["name"], 'user_email': result["email"],'exp': datetime.datetime.now() + datetime.timedelta(hours=12)}, app.config['SECRET_KEY'])
    return make_response(
        jsonify(
	    message='Access Garanted!',
            data=jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"]),
            exp=datetime.datetime.now() + datetime.timedelta(hours=12),
            token=token
        )
    )

@app.route('/license', methods=['POST'])
def get_license():
    input_data = request.json
    result = verify_login(input_data["id"], input_data["user"], input_data["password"], input_data["account"])
    if result != "Access garantee":
        return make_response(
            jsonify(
		message='Bad Request',
                data=result
            )
        )
    

    # encode license number
 
    S = 3  # number of characters in the string.
    T = 2 # number of characters in the string.

    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))

    ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k = T))

    # enter month and year of expiration
    credentials = get_credentials(input_data["id"])
    know_user = credentials
    mm = 0
    yyyy = 0
    try:
        mm = int(know_user["exp_month"])
        yyyy = int(know_user["exp_year"])
    except:
        return make_response(
            jsonify("Invalid number.")
        )

    # doing conversions and calculations
    str_yyyy = str(yyyy)
    yyy = str_yyyy[0] + str_yyyy[1] + str_yyyy[2]
    y = str_yyyy[3]

    lic_mm = str(mm + 16)
    lic_yyy = int(yyy, 10) + 987
    lic_yyyy = str(lic_yyy) + str(y)

    # final lic number
    lic = str(ran) + lic_mm + lic_yyyy + str(ran2)

    return make_response(
        jsonify(lic)
    )

@app.route('/user/insert', methods=['POST'])
@token_required
def insert_user():
    input_data = request.json
    result = post_create_user(input_data["id"],input_data["name"],input_data["email"],input_data["password"],input_data["accounts"],input_data["exp_month"],input_data["exp_year"])
    response = make_response(
        jsonify(
            message="success",
            data=json.loads(json_util.dumps(result))
        )
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/user/id', methods=['POST'])
@token_required
def get_user():
    input_data = request.json
    result = get_credentials(input_data["id"])

    response = make_response(
        jsonify(
            message="success",
            data=json.loads(json_util.dumps(result))
        )
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/user/all', methods=['GET'])
@token_required
def get_all_users():
    result = get_get_all_users()

    response = make_response(
        jsonify(
            message="success",
            data=json.loads(json_util.dumps(result))
        )
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/user/update', methods=['PUT'])
@token_required
def update_user():
    input_data = request.json
    result = put_update_user(input_data["id"],input_data["name"],input_data["email"],input_data["password"],input_data["accounts"],input_data["exp_month"],input_data["exp_year"])
    response = make_response(
        jsonify(
            message="success",
            data=json.loads(json_util.dumps(result))
        )
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/user/delete/id', methods=['DELETE'])
@token_required
def delete_user():
    input_data = request.json
    result = del_delete_user(input_data["id"])
    response = make_response(
        jsonify(
            message="success",
            data=json.loads(json_util.dumps(result))
        )
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run(port=8080)
