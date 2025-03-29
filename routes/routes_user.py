from flask import request, jsonify,Blueprint
from helper_function.jwt_initialization import create_token
from modules.user import get_user, insert_user, delete_user, update_user
from helper_function.utility import search_music, search_musician, search_user, get_musician_catalogue, get_all_users, get_musicians
from helper_function.celery_file import process_payment
from datetime import datetime
# from helper_function.redis_config import redis_user_payment #no longer using redis so i commented it
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


# intialize the user blueprint
user_bp = Blueprint('user', __name__)


#test the user route is running
@user_bp.route('/')
def index():
    return "user routes is running"


#route to process the payment
@user_bp.route('/payment_processed', methods=['POST'])
def payment_processed():
    data = request.json # get json data
    user_expiry_date = data['user_expiry_date'] # get the user expiry date from json data
   
   
    try:
        account_name = data['account_name']
        account_number = data['account_number']
        cvv = data['cvv']
        password = data['password']
        amount_in_account = data['amount_in_account']
        expiry_date = datetime.strptime(user_expiry_date, "%d/%m/%Y")

    except KeyError:
        return jsonify({"message": "All fields are required"}), 400    
    except ValueError:
        return jsonify({"message": "Invalid data format"}), 400
    # the process payment was supposed to be done with celery but we could not get a background worker, below was the code to do that:

    # task = process_payment.apply_async(args=[account_name, account_number, cvv, password, expiry_date, amount_in_account])
    # return jsonify({"message": "payment processing started", "task_id": task.id}), 202

    #process payment done normally, the frontend would wait till it sends a success message then it generate an id to imitate the task id celery was suppose to generate
    result = process_payment(account_name, account_number, cvv, password, expiry_date, amount_in_account)
    return jsonify(result), 200  # return the process payment response

#the task_payment status would have checked for the status and if it was success send it with the task id to the frontend 

# @user_bp.route('/payment_status/<task_id>', methods=['GET'])
# def payment_status(task_id):

#     task = process_payment.AsyncResult(task_id)

#     if task.state == "PENDING":
#         return jsonify({"STATUS": "processing payment"}), 202
    
#     elif task.state == "SUCCESS":

#         redis_user_payment.setex(f"task_id:{task_id}", 3600, "verified")
#         return jsonify({"STATUS": f"payment processes, task id is:{task_id}. Don't forget to copy task_id"}), 200
    
#     else:
#         return jsonify({"STATUS": task.state}), 400
    

#route to add user
@user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    data =  request.json #get json data from frontend
    task_id = data.get('task_id')  #get the task id from the json data

    if not task_id:

        return jsonify({"status": "error", "message": "Task ID is required"}), 400 # return error message if no task id was gotten
    
    # if redis_user_payment.get(f"task_id:{task_id}") == "verified":

    response, status_code = insert_user(data) #call the insert user to get the response whether it was successful or an error
    return jsonify (response), status_code # return the response
    
    # else:
    #     return jsonify ({"status": "error", "message": "Invalid Task ID. Complete payment first"}), 400


#route to authenticate or validate the user
@user_bp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    data = request.json #get json data from frontend
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user_details = get_user(username) #get the user details and store it

        if check_password_hash(user_details['password'], password):  #validate password
            access_token = create_token(id=username) #create the access token with the username as identity
            return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200 #return success and the access token if succesful
        else:
            return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401    
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

#route to display the user profile
@user_bp.route('/user_profile', methods=['GET'])
@jwt_required()#add jwt decorator to make sure jwt is valid 
def user_profile():
    user = get_jwt_identity() # get the identity and store it

    if user:
        user_details = get_user(user) #get the user details and store it
        if user_details:
            user_details['_id'] = str(user_details['_id']) #make _id to be string to allow json to read it
            return jsonify(user_details), 200 # return details
        else:
            return jsonify({"status": "error", "message": "Couldn't get details"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access Denied"}), 401
    

#route to search a user   
@user_bp.route('/search_user', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def search_a_user():
    data = request.json #get json data from frontend
    user_to_search = data.get('user_to_search')
    user = get_jwt_identity() # get the identity and store it

    response, status_code = search_user(user, user_to_search) #call the search user to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to get all the users
@user_bp.route('/get_users', methods=['GET'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def get_users():
    user = get_jwt_identity() # get the identity and store it

    response, status_code = get_all_users(user)  #call the get all user to get the response whether it was successful or an error
    return jsonify(response), status_code  # return the response


#route to search musician
@user_bp.route('/search_musician', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def search_a_musician(): 
    user = get_jwt_identity()  # get the identity and store it
    data = request.json #get json data from frontend
    musician_name = data.get('musician')

    response, status_code =  search_musician(user, musician_name) #call the search musician to get the response whether it was successful or an error
    return jsonify(response), status_code   # return the response


#route to get all the musician
@user_bp.route('/get_musicians', methods=['GET'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def get_all_musicians():
    user = get_jwt_identity() # get the identity and store it
    
    response, status_code = get_musicians(user) #call the get musicians to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to search music
@user_bp.route('/search_music', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def search_a_music():
    data = request.json #get json data from frontend
    music_details = data.get('music_details')
    user = get_jwt_identity() # get the identity and store it

    response, status_code = search_music(user, music_details) #call the search music to search music and get the response whether it was successful or an error
    return jsonify(response), status_code  # return the response


#route to get musician catalogue
@user_bp.route('/get_musician_catalogue', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def get_a_musician_catalogue():
    data = request.json #get json data from frontend
    user = get_jwt_identity()  # get the identity and store it
    musician_name = data.get('musician_name')

    response, status_code = get_musician_catalogue(user, musician_name) #call the get musician caalogue to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response
    

#route to update user info
@user_bp.route('/update_user_info', methods=['PUT'])
def update_user_info():
    data = request.json  #get json data from frontend
    user = data.get('user') 
    details = data.get('details')

    if user:
        if details:
            response, status_code = update_user(user, details) #call the update user to update user and get the response whether it was successful or an error
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


#route to delete the user details
@user_bp.route('/delete_user_details', methods=['DELETE'])
@jwt_required() #add jwt decorator to make sure jwt is valid             
def delete_user_details():
    user = get_jwt_identity() # get the identity and store it
    data = request.json #get json data from frontend
    password = data.get('password')

    if user:
        if password:
            response, status_code = delete_user(user, password) # call the delete user to delete user
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401

