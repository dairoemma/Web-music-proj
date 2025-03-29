from flask import request, jsonify, Blueprint
from helper_function.jwt_initialization import create_token
from modules.musician import  get_musician, insert_musician, delete_musician, update_music, update_musician, add_music, delete_music
from datetime import datetime
from helper_function.celery_file import process_payment
# from helper_function.redis_config import redis_musician_payment  #no longer using redis so i commented it
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper_function.utility import search_music, search_musician, search_user, get_musician_catalogue, get_all_users, get_musicians


# intialize the musician blueprint
musician_bp = Blueprint('musician', __name__)


#test the musician route is running
@musician_bp.route('/')
def index():
    return "musician routes is running"


#route to process the payment
@musician_bp.route('/payment_processed', methods=['POST'])
def payment_processed():
    data = request.json # get json data
    musician_expiry_date = data['user_expiry_date'] # get the musician expiry date from json data
   
   
    try:
        account_name = data['account_name']
        account_number = data['account_number']
        cvv = data['cvv']
        password = data['password']
        amount_in_account = data['amount_in_account']
        expiry_date = datetime.strptime(musician_expiry_date, "%d/%m/%Y")

    except KeyError:
        return jsonify({"message": "All fields are required"}), 400    
    except ValueError:
        return jsonify({"message": "Invalid data format"}), 400

    # the process payment was supposed to be done with celery but we could not get a background worker, below was the code to do that:

    # task = process_payment.apply_async(args=[account_name, account_number, cvv, password, expiry_date, amount_in_account])
    # return jsonify({"message": "payment processing started", "task_id": task.id}), 202

    #process payment done normally, the frontend would wait till it sends a success message then it generate an id to imitate the task id celery was suppose to generate
    result = process_payment(account_name, account_number, cvv, password, expiry_date, amount_in_account)
    return jsonify(result), 200 # return the process payment response


#the task_payment status would have checked for the status and if it was success send it with the task id to the frontend 

# @musician_bp.route('/payment_status/<task_id>', methods=['GET'])
# def payment_status(task_id):

#     task = process_payment.AsyncResult(task_id)

#     if task.state == "PENDING":
#         return jsonify({"STATUS": "processing payment"}), 202
    
#     elif task.state == "SUCCESS":

#         redis_musician_payment.setex(f"task_id:{task_id}", 3600, "verified")
#         return jsonify({"STATUS": f"payment processes, task id is:{task_id}. Don't forget to copy task_id"}), 200
    
#     else:
#         return jsonify({"STATUS": task.state}), 400   


#route to add musician
@musician_bp.route('/add_musician', methods=['GET', 'POST'])
def add_musician():
    data =  request.json #get json data from frontend
    task_id = data.get('task_id') #get the task id from the json data

    if not task_id:

        return jsonify({"status": "error", "message": "Task ID is required"}), 400 # return error message if no task id was gotten
    
    # if redis_musician_payment.get(f"task_id:{task_id}") == "verified":

    response, status_code = insert_musician(data) #call the insert musician to get the response whether it was successful or an error
    return jsonify (response), status_code # return the response
    
    # else:
    #     return jsonify ({"status": "error", "message": "Invalid Task ID. Complete payment first"}), 400


#route to authenticate or validate the musician
@musician_bp.route('/authenticate_musician', methods=['POST'])
def authenticate_musician():
    data = request.json #get json data from frontend
    music_name = data.get('music_name')
    password = data.get('password')

    if music_name and password:
        musician_details = get_musician(username=music_name) #get the musician details and store it

        if check_password_hash(musician_details['password'], password):  #validate password
            access_token = create_token(id=music_name) # create the access token with the musicianname as identity
            return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200  #return success and the access token if succesful
        else:
            return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401
            
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

#route to display the musician profile
@musician_bp.route('/musician_profile', methods=['GET'])
@jwt_required()#add jwt decorator to make sure jwt is valid 
def musician_profile():
    musician = get_jwt_identity() # get the identity and store it

    if musician:
        musician_details = get_musician(musician) #get the musician details and store it
        if musician_details:
            musician_details['_id'] = str(musician_details['_id']) #make _id to be string to allow json to read it
        return jsonify(musician_details), 200  # return details 
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access Denied"}), 401
    

#route to search a user   
@musician_bp.route('/search_user', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def search_a_user():
    data = request.json #get json data from frontend
    user_to_search = data.get('user_to_search')
    musician = get_jwt_identity()  # get the identity and store it

    response, status_code = search_user(musician, user_to_search) #call the search user to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to get all the users
@musician_bp.route('/get_users', methods=['GET'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def get_users():
    musician = get_jwt_identity() # get the identity and store it

    response, status_code = get_all_users(musician) #call the get all user to get the response whether it was successful or an error
    return jsonify(response), status_code  # return the response


#route to search musician
@musician_bp.route('/search_musician', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def search_a_musician():
    musician = get_jwt_identity() # get the identity and store it
    data = request.json #get json data from frontend
    musician_name = data.get('musician')

    response, status_code =  search_musician(musician, musician_name) #call the search musician to get the response whether it was successful or an error
    return jsonify(response), status_code  # return the response


#route to get all the musician
@musician_bp.route('/get_musicians', methods=['GET'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def get_all_musicians():
    musician = get_jwt_identity() # get the identity and store it

    response, status_code = get_musicians(musician)#call the get musicians to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to search music
@musician_bp.route('/search_music', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def search_a_music():
    data = request.json #get json data from frontend
    music_details = data.get('music_details')
    musician = get_jwt_identity()  # get the identity and store it
    
    response, status_code = search_music(musician, music_details) #call the search music to search music and get the response whether it was successful or an error
    return jsonify(response), status_code  # return the response


#route to get musician catalogue
@musician_bp.route('/get_musician_catalogue', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def get_a_musician_catalogue():
    data = request.json #get json data from frontend
    musician = get_jwt_identity()  # get the identity and store it
    musician_name = data.get('musician_name')

    response, status_code = get_musician_catalogue(musician, musician_name)  #call the get musician caalogue to get the response whether it was successful or an error
    return jsonify(response), status_code # return the response


#route to update musician info
@musician_bp.route('/update_musician_info', methods=['PUT'])
def update_musician_info():
    data = request.json #get json data from frontend
    musician = data.get('musician') 
    details = data.get('details')

    if musician:

        if details:
            response, status_code = update_musician(musician, details) #call the update musician to update musician and get the response whether it was successful or an error
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401

#route to update music info
@musician_bp.route('/update_music', methods=['PUT'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def update_music_info():
    musician = get_jwt_identity() # get the identity and store it
    song_name = request.form.get("song_name") #get song_name data from frontend
    file = request.files.get("file") #get file data from frontend

    if not musician:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401

    if not song_name or not file:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    
    temp_path = f"/tmp/{file.filename}" #store the file path in temp_path 

    try:
        file.save(temp_path) # save it to the file object
        result = update_music(musician, song_name, temp_path) #call the update music to update music and get the response whether it was successful or an error

        if result is None:
            return jsonify({"status": "error", "message": "Unexpected failure in update_music"}), 500

        return result  # return result if not none
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

#route to delete music 
@musician_bp.route('/delete_music', methods=['POST'])
@jwt_required()#add jwt decorator to make sure jwt is valid
def delete_musics():
    musician = get_jwt_identity() # get the identity and store it
    data = request.json #get json data from frontend
    password = data.get('password')
    song_name = data.get('song_name')

    if musician:

        if password and song_name:
            response, status_code = delete_music(musician, password, song_name) #call the delete music to delete music and get the response whether it was successful or an error
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


#route to add music 
@musician_bp.route('/add_music', methods=['POST'])
@jwt_required() #add jwt decorator to make sure jwt is valid
def add_musics():
    musician = get_jwt_identity() # get the identity and store it
    song_name = request.form.get("song_name") #get song_name data from frontend
    file = request.files.get("file") #get file data from frontend
    
    if not musician:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401

    if not song_name or not file:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    temp_path = f"/tmp/{file.filename}"  #store the file path in temp_path 
 
    try:
        file.save(temp_path) # save it to the file object

        result = add_music(musician, song_name, temp_path) #call the add music to add music and get the response whether it was successful or an error

        if result is None:
            return jsonify({"status": "error", "message": "Unexpected failure in add_music"}), 500

        return result  # return result if not none

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

#route to delete the musician details
@musician_bp.route('/delete_musician_details', methods=['DELETE'])
@jwt_required()  #add jwt decorator to make sure jwt is valid    
def delete_musician_details():
    musician = get_jwt_identity() # get the musician details
    data = request.json # get the identity and store it
    password = data.get('password')

    if musician:

        if password:
            response, status_code = delete_musician(musician, password) # call the delete musician to delete musician
            return jsonify(response), status_code # return the response
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401
