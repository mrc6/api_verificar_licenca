from pymongo import MongoClient
from bson.objectid import ObjectId

def get_connection():
    try: 
        conn = MongoClient()  # Making connection
    except: 
        print("Could not connect to MongoDB")
    return conn

def get_login(email):
    client = get_connection()
    db = client.expert_advisor
    user = db.login.find_one({"email": email})
    return user
    client.close()

def get_credentials(user_id):
    client = get_connection()
    db = client.expert_advisor
    user = db.users.find_one({"id": user_id})
    return user
    client.close()

def get_get_all_users():
    client = get_connection()
    db = client.expert_advisor
    data = []
    for x in db.users.find({}, {"_id":0, "id": 1, "name": 1, "email": 1, "exp_month": 1, "exp_year": 1 }):
        data.append(x)
    return data
    client.close()

def post_create_user(id,name,email,password,accounts,exp_month,exp_year):
    client = get_connection()
    db = client.expert_advisor
    accounts_str = accounts.replace(" ", "")
    accounts_array = accounts_str.split(',')
    user = db.users.insert_one({"id": id, "name": name, "email": email, "password": password,"accounts": accounts_array, "exp_month": exp_month, "exp_year": exp_year}).inserted_id
    return ObjectId(user)
    client.close()

def put_update_user(id,name,email,password,accounts,exp_month,exp_year):
    client = get_connection()
    db = client.expert_advisor
    accounts_str = accounts.replace(" ", "")
    accounts_array = accounts_str.split(',')
    filter = { "id": id }
    user_new_values = { "$set": {"id": id, "name": name, "email": email, "password": password,"accounts": accounts_array, "exp_month": exp_month, "exp_year": exp_year}}
    user = db.users.update_one(filter, user_new_values)
    return "User updated!!!"
    client.close()

def del_delete_user(id):
    client = get_connection()
    db = client.expert_advisor
    filter = { "id": id }
    user = db.users.delete_one(filter)
    return "User deleted!!!"
    client.close()
