from modules.database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash



def get_all_user():
    users = users_collection.find()
    user_dict = {user["username"]:user for user in users}
    return user_dict


def get_user(username):
    user = users_collection.find_one({"username": username})
    
    if user:
        return user
    else:
        return {"status": "error", "message": "Username doesn't exist"}, 404


def insert_user(user_details):
    name = user_details['name']
    username = user_details['username']
    password = user_details['password']
    email = user_details['email']

    if name and username and password and email:
        
        if get_user(username):
           return {"status": "error", "message": "Username already exist"}, 400 
        
        else: 
             hashed_password = generate_password_hash(password)
             users_collection.insert_one({"name": name, "username": username, "password": hashed_password, "email": email})
             return {"status": "success", "message": "user added successfully"}, 201
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

def delete_user(username, password):
    if username and password:
        user_get_detail = get_user(username=username)

        if user_get_detail:

            if user_get_detail['username'] == username and check_password_hash(user_get_detail['password'], password):
                users_collection.delete_one({"username":username})
                return {"status": "success", "message": "user deleted successfully"}, 200
            else:
                return {"status": "error", "message": "Incorrect username or password"}, 401
            
        else:
            return {"status": "error", "message": "Username does not exist"}, 404    
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

def update_user(username, user_details):
    field_to_update = user_details['field_to_update']
    field_new_value = user_details['field_new_value']

    if username and field_to_update and field_new_value:

        if get_user(username=username):

            if field_to_update == "password":
                user_password = field_new_value
                hashed_password = generate_password_hash(user_password)
                users_collection.update_one({"musician_name": username}, {"$set": {"password": hashed_password}})
                return {"status": "success", "message": "user password updated successfully"}, 200
            else:
                users_collection.update_one({"username": username}, {"$set": {field_to_update: field_new_value}})
                return {"status": "success", "message": "user updated successfully"}, 200
            
        else:
            return {"status": "error", "message": "Username does not exist"},404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
    
    

           
        
     
    
