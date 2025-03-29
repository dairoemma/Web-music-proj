from modules.database import admins_collection
from werkzeug.security import generate_password_hash, check_password_hash

#function to get all the admin from the database
def get_all_admin():
   admins = admins_collection.find() #query to search the admins collection snd return all document
   admin_dict = {}

   for admin in admins:
        admin['_id'] = str(admin['_id'])  
        admin_dict[admin["username"]] = admin # store the admin in a dict

   return admin_dict #return the dict

#function to get an admin from the database
def get_admin(username):
    admin = admins_collection.find_one({"username": username}) #the query to search the admins collection and return an admin document
    
    if admin:
        return admin #return the admin
    else:
        return {"status": "error", "message": "Admin name doesn't exist"}, 404

#function to insert an admin to the database
def insert_admin(admin_details):
    # get all the details
    username = admin_details['username']
    password = admin_details['password']
    email = admin_details['email']

    if username and password and email:
        admin = get_admin(username) #we used the get admin to check if the user already exist
        if isinstance(admin, dict) and admin.get("status") != "error":
            return {"status": "error", "message": "admin already exist"}, 400 #return an error admin already exist response and 400 status code
        else:
            hashed_password = generate_password_hash(password) #generate the hashed password
            admins_collection.insert_one({
                "username": username,
                "password": hashed_password,
                "email": email
            })# run the query to insert the admin
            return {"status": "success", "message": "admin added successfully"}, 201
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
#function to delete a admin in the database
def delete_admin(username, password):
    if username and password:
        admin_get_detail = get_admin(username=username)# check if admin already exist

        if admin_get_detail:

            if admin_get_detail['username'] == username and check_password_hash(admin_get_detail['password'], password): #check if the username and the username password matches the admin and is password given
                admins_collection.delete_one({"username": username})#run the query to delete the admin
                return {"status": "success", "message": "Admin deleted successfully"}, 200
            else:
                return {"status": "error", "message": "Incorrect username or password"}, 401
            
        else:
            return {"status": "error", "message": "Username does not exist"}, 404    
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
#function to update an admin in the database
def update_admin(username, admin_details):
    # get all the details
    field_to_update = admin_details['field_to_update']
    field_new_value = admin_details['field_new_value']

    if username and field_to_update and field_new_value:
        admin = get_admin(username)#we used the get admin to check if the user exist
        if isinstance(admin, dict) and admin.get("status") != "error":
            if field_to_update == "password": # if field to update is the password, it should update it seperately because we want to hash the password first
                admin_password = field_new_value
                hashed_password = generate_password_hash(admin_password)
                admins_collection.update_one({"username": username}, {"$set": {"password": hashed_password}})#run the query to update the password
                return {"status": "success", "message": "admin password updated successfully"}, 200
            else:
                admins_collection.update_one({"username": username}, {"$set": {field_to_update: field_new_value}})#run the query to update the admin
                return {"status": "success", "message": "admin updated successfully"}, 200
            
        else:
            return {"status": "error", "message": "Username does not exist"}, 404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
    
    

           
        
     
    
