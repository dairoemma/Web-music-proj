from flask import request, jsonify, Blueprint
from helper_function.jwt_initialization import create_token
from modules.admin import get_admin, get_all_admin, insert_admin, delete_admin, update_admin
from helper_function.utility import search_music, search_musician, search_user, get_musician_catalogue, get_all_users, get_musicians
from modules.user import delete_user
from modules.musician import delete_musician
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


# intialize the admin blueprint
admin_bp = Blueprint('admin', __name__)


#test the admin route is running
@admin_bp.route('/')
def index():
    return "admin routes is running"


#route to add admin
@admin_bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    data =  request.json #get json data from frontend

    response, status_code = insert_admin(data) #call the insert admin to get the response whether it was successful or an error
    return jsonify (response), status_code # return the response


#route to authenticate or validate the admin
@admin_bp.route('/authenticate_admin', methods=['POST'])
def authenticate_admin():
    data = request.json #get json data from frontend
    username = data.get('username')
    password = data.get('password')

    if username and password:
        admin_details = get_admin(username) #get the admin details and store it

        if check_password_hash(admin_details['password'], password): #validate password
            access_token = create_token(id=username) # create the access token with the username as identity
            return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200 #return success and the access token if succesful
        else:
            return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401    
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

#route to display the admin profile
@admin_bp.route('/admin_profile', methods=['GET'])
@jwt_required() #add jwt decorator to make sure jwt is valid 
def admin_profile():
    admin = get_jwt_identity() # get the identity and store it

    if admin:
        admin_details = get_admin(admin) #get the admin details and store it
        if admin_details:
            admin_details['_id'] = str(admin_details['_id']) #make _id to be string to allow json to read it
        return jsonify(admin_details), 200 # return details 
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access Denied"}), 401
    

#route to get all admin
@admin_bp.route('/get_all_admin', methods=['GET'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def get_all_admins():
    admin = get_jwt_identity() # get the identity and store it
    
    if admin:
        admin_list = get_all_admin()  #get all the admin details and store it
        return jsonify(admin_list), 200 # return details 
    else:
        return jsonify({"status": "error", "message": "Invalid credential, Access denied"}), 401


#route to search a user
@admin_bp.route('/search_user', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def search_a_user():
    data = request.json  #get json data from frontend
    user_to_search = data.get('user_to_search')
    admin = get_jwt_identity() # get the identity and store it

    response, status_code = search_user(admin, user_to_search) #call the search user to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to get all the users
@admin_bp.route('/get_users', methods=['GET'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def get_users():
    admin = get_jwt_identity() # get the identity and store it

    response, status_code = get_all_users(admin) #call the get all user to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to search musician
@admin_bp.route('/search_musician', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def search_a_musician():
    admin = get_jwt_identity() # get the identity and store it
    data = request.json #get json data from frontend
    musician_name = data.get('musician')

    response, status_code =  search_musician(admin, musician_name) #call the search musician to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response

#route to get all the musician
@admin_bp.route('/get_musicians', methods=['GET'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def get_all_musicians():
    admin = get_jwt_identity() # get the identity and store it
    
    response, status_code = get_musicians(admin)#call the get musicians to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to search music
@admin_bp.route('/search_music', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def search_a_music():
    data = request.json #get json data from frontend
    music_details = data.get('music_details')
    admin = get_jwt_identity() # get the identity and store it

    response, status_code = search_music(admin, music_details) #call the search music to search music and get the response whether it was successful or an error
    return jsonify(response), status_code  # return the response


#route to get musician catalogue
@admin_bp.route('/get_musician_catalogue', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def get_a_musician_catalogue():
    data = request.json #get json data from frontend
    admin = get_jwt_identity()  # get the identity and store it
    musician_name = data.get('musician_name')

    response, status_code = get_musician_catalogue(admin, musician_name) #call the get musician caalogue to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response
    

#route to update admin info
@admin_bp.route('/update_admin_info', methods=['PUT'])
def update_admin_info():
    data = request.json #get json data from frontend
    admin = data.get('admin') 
    details = data.get('details')

    if admin:
        if details:
            response, status_code = update_admin(admin, details) #call the update admin to update admin and get the response whether it was successful or an error
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


#route to delete the user details
@admin_bp.route('/delete_user_details', methods=['DELETE'])
@jwt_required()#add jwt decorator to make sure jwt is valid      
def delete_user_details():
    admin  = get_jwt_identity()  # get the identity and store it
    data = request.json #get json data from frontend
    password = data.get('password')
    user_to_delete = data.get('user_to_delete')
    admin_details = get_admin(admin) # get the admin details

    if admin_details:
        if check_password_hash(admin_details['password'], password): # validate password sent by json is the same as the admin details password
            response, status_code = delete_user(user_to_delete, force=True)# call the delete user to delete user
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status":"error", "message": "Invalid password"}), 401
        
    else:
        return jsonify({"status": "error", "message": "Invalid admin, Access denied"}), 401


#route to delete the musician details
@admin_bp.route('/delete_musician_details', methods=['DELETE'])
@jwt_required() #add jwt decorator to make sure jwt is valid        
def delete_musician_details():
    admin  = get_jwt_identity() # get the identity and store it
    data = request.json #get json data from frontend
    password = data.get('password')
    musician_to_delete = data.get('user_to_delete')
    admin_details = get_admin(admin)   # get the admin details

    if admin_details:
        if check_password_hash(admin_details['password'], password): # validate password sent by json is the same as the admin details password
            response, status_code = delete_musician(musician_to_delete, force=True) # call the delete musician to delete musician
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status":"error", "message": "Invalid password"}), 401
        
    else:
        return jsonify({"status": "error", "message": "Invalid admin, Access denied"}), 401
    

#route to delete the admin details
@admin_bp.route('/delete_admin_details', methods=['DELETE'])
@jwt_required() #add jwt decorator to make sure jwt is valid       
def delete_admin_details():
    admin = get_jwt_identity() # get the identity and store it
    data = request.json #get json data from frontend
    password = data.get('password')

    if admin:
        if password:
            response, status_code = delete_admin(admin, password) # call the delete admin to delete admin
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status":"error", "message": "Invalid password"}), 401
              
    else:
        return jsonify({"status": "error", "message": "Invalid admin, Access denied"}), 401
