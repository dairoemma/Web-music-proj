from modules.database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash


#function to get all the user from the database
def get_all_user():
    users = users_collection.find() #query to search the users collection and return all document
    users_dict = {}

    for user in users:
        user['_id'] = str(user['_id'])  
        users_dict[user["username"]] = user # store the user in a dict
    
    return users_dict #return the dict


#function to get an admin from the database
def get_user(username):
    user = users_collection.find_one({"username": username}) #the query to search the users collection and return a user document
    
    if user:
        return user #return the user
    else:
        return {"status": "error", "message": "Username doesn't exist"}, 404


#function to insert a user to the database
def insert_user(user_details):
    # get all the details
    name = user_details['name']
    username = user_details['username']
    password = user_details['password']
    email = user_details['email']

    if name and username and password and email:
        user = get_user(username) #we used the get user to check if the user already exist
        if isinstance(user, dict) and user.get("status") != "error":
            return {"status": "error", "message": "Username already exist"}, 400 #return an error user already exist response and 400 status code
        else:
            hashed_password = generate_password_hash(password)#generate the hashed password
            users_collection.insert_one({
                "name": name,
                "username": username,
                "password": hashed_password,
                "email": email
            }) # run the query to insert the user
            return {"status": "success", "message": "user added successfully"}, 201

    else:
        return {"status": "error", "message": "All fields are required"}, 400
    

#function to delete a user in the database
def delete_user(username, password=None, force=False):
    user = get_user(username) # check if user already exist

    if not user:
        return {"status": "error", "message": "User does not exist"}, 404 #return user doesn't exist if user is none

    if force or (password and check_password_hash(user['password'], password)):#check if the username and the username password matches the user and is password given and if force is true to give admin priviledge
        users_collection.delete_one({"username": username})#run the query to delete the user
        return {"status": "success", "message": "User deleted successfully"}, 200
    else:
        return {"status": "error", "message": "Incorrect password"}, 401
    
#function to update a user in the database
def update_user(username, user_details):
    # get all the details
    field_to_update = user_details['field_to_update']
    field_new_value = user_details['field_new_value']

    if username and field_to_update and field_new_value:

        user = get_user(username) #we used the get user to check if the user exist
        if isinstance(user, dict) and user.get("status") != "error":
            if field_to_update == "password": # if field to update is the password, it should update it seperately because we want to hash the password first
                user_password = field_new_value
                hashed_password = generate_password_hash(user_password)
                users_collection.update_one({"musician_name": username}, {"$set": {"password": hashed_password}})#run the query to update the password
                return {"status": "success", "message": "user password updated successfully"}, 200
            else:
                users_collection.update_one({"username": username}, {"$set": {field_to_update: field_new_value}})#run the query to update the admin
                return {"status": "success", "message": "user updated successfully"}, 200
            
        else:
            return {"status": "error", "message": "Username does not exist"},404 
        
    else:
        return {"status": "error", "message": "All fields are required"}, 400
    
    
    

           
        
     
    
