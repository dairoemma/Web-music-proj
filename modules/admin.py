from modules.database import admins_collection
from werkzeug.security import generate_password_hash, check_password_hash


def get_all_admin():
    admins = admins_collection.find()
    admins_dict = {admin["username"]: admin for admin in admins}
    return admins_dict


def get_admin(username):
    admin = admins_collection.find_one({"username": username})
    
    if admin:
        return admin
    else:
        return None


def insert_admin(admin_details):
    username = admin_details['username']
    password = admin_details['password']
    email = admin_details['email']

    if username and password and email:
        
        if get_admin(username=username):
            return {"status": "error", "message": "Username already exist"}, 400 
            
        else:
            hashed_password = generate_password_hash(password)
            admins_collection.insert_one({"username": username, "password": hashed_password, "email": email})
            return {"status": "success", "message": "admin added successfully"}, 201
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

def delete_admin(username, password):
    if username and password:
        admin_get_detail = get_admin(username=username)

        if admin_get_detail:

            if admin_get_detail['username'] == username and check_password_hash(admin_get_detail['password'], password):
                admins_collection.delete_one({"username": username})
                return {"status": "success", "message": "Admin deleted successfully"}, 200
            else:
                return {"status": "error", "message": "Incorrect username or password"}, 401
            
        else:
            return {"status": "error", "message": "Username does not exist"}, 400    
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

def update_admin(username, admin_details):
    field_to_update = admin_details['field_to_update']
    field_new_value = admin_details['field_new_value']

    if username and field_to_update and field_new_value:

        if get_admin(username=username):
            if field_to_update == "password":
                admin_password = field_new_value
                hashed_password = generate_password_hash(admin_password)
                admins_collection.update_one({"username": username}, {"$set": {"password": hashed_password}})
                return {"status": "success", "message": "admin password updated successfully"}, 200
            else:
                admins_collection.update_one({"username": username}, {"$set": {field_to_update: field_new_value}})
                return {"status": "success", "message": "admin updated successfully"}, 200
            
        else:
            return {"status": "error", "message": "Username does not exist"}, 400 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
    
    

           
        
     
    
