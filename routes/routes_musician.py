from flask import request, jsonify, Blueprint
from helper_function.jwt_initialization import create_token
from modules.musician import  get_musician, insert_musician, delete_musician, update_music, update_musician, add_music, delete_music
from datetime import datetime
from helper_function.celery_file import process_payment
from helper_function.redis_config import redis_musician_payment
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper_function.utility import search_music, search_musician, search_user, get_musician_catalogue, get_all_users, get_musicians
from helper_function.socket_file import on_connect, handle_leave_room, handle_message


musician_bp = Blueprint('musician', __name__)


@musician_bp.route('/')
def index():
    return "musician routes is running"


@musician_bp.route('/payment_processed', methods=['POST'])
def payment_processed():
    data = request.json
    musician_expiry_date = data['user_expiry_date']
   
   
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

    # task = process_payment.apply_async(args=[account_name, account_number, cvv, password, expiry_date, amount_in_account])
    # return jsonify({"message": "payment processing started", "task_id": task.id}), 202
    result = process_payment(account_name, account_number, cvv, password, expiry_date, amount_in_account)
    return jsonify(result), 200 


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


@musician_bp.route('/add_musician', methods=['GET', 'POST'])
def add_musician():
    data =  request.json
    task_id = data.get('task_id')

    if not task_id:

        return jsonify({"status": "error", "message": "Task ID is required"}), 400
    
    # if redis_musician_payment.get(f"task_id:{task_id}") == "verified":

    response, status_code = insert_musician(data)
    return jsonify (response), status_code
    
    # else:
    #     return jsonify ({"status": "error", "message": "Invalid Task ID. Complete payment first"}), 400


@musician_bp.route('/authenticate_musician', methods=['POST'])
def authenticate_musician():
    data = request.json
    music_name = data.get('music_name')
    password = data.get('password')

    if music_name and password:
        musician_details = get_musician(username=music_name)
        if musician_details:
            stored_password = musician_details.get('password', '')
            if check_password_hash(musician_details['password'], password) or stored_password == password:
                access_token = create_token(id=music_name)
                return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200
            else:
                return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401
        else:
            return jsonify({"status": "error", "message": "Musician name not found"}), 404    
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

@musician_bp.route('/musician_profile', methods=['GET'])
@jwt_required()
def musician_profile():
    musician = get_jwt_identity()

    if musician:
        musician_details = get_musician(musician)
        return jsonify(musician_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access Denied"}), 401
    
    
@musician_bp.route('/search_user', methods=['GET'])
@jwt_required()
def search_a_user():
    data = request.json
    user_to_search = data.get('user_to_search')
    musician = get_jwt_identity()

    response, status_code = search_user(musician, user_to_search)
    return jsonify(response), status_code


@musician_bp.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    musician = get_jwt_identity()

    response, status_code = get_all_users(musician)
    return jsonify(response), status_code


@musician_bp.route('/search_musician', methods=['GET'])
@jwt_required()
def search_a_musician():
    musician = get_jwt_identity()
    data = request.json
    musician_name = data.get('musician')

    response, status_code =  search_musician(musician, musician_name)
    return jsonify(response), status_code


@musician_bp.route('/get_musicians', methods=['GET'])
@jwt_required()
def get_all_musicians():
    musician = get_jwt_identity()

    response, status_code = get_musicians(musician)
    return jsonify(response), status_code


@musician_bp.route('/search_music', methods=['GET'])
@jwt_required()
def search_a_music():
    data = request.json
    music_details = data.get('music_details')
    musician = get_jwt_identity()
    
    response, status_code = search_music(musician, music_details)
    return jsonify(response), status_code


@musician_bp.route('/get_musician_catalogue', methods=['GET'])
@jwt_required()
def get_a_musician_catalogue():
    data = request.json
    musician = get_jwt_identity()
    musician_name = data.get('musician_name')

    response, status_code = get_musician_catalogue(musician, musician_name)
    return jsonify(response), status_code


@musician_bp.route('/update_musician_info', methods=['PUT'])
@jwt_required()
def update_musician_info():
    musician = get_jwt_identity()
    data = request.json
    details = data.get('details')

    if musician:

        if details:
            response, status_code = update_musician(musician, details)
            return jsonify(response), status_code
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@musician_bp.route('/update_music', methods=['PUT'])
@jwt_required()
def update_music_info():
    musician = get_jwt_identity()
    data = request.json
    details = data.get('details')

    if musician:

        if details:
            response, status_code = update_music(musician, details)
            return jsonify(response), status_code
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@musician_bp.route('/delete_music', methods=['POST'])
@jwt_required()
def delete_musics():
    musician = get_jwt_identity()
    data = request.json
    password = data.get('password')
    song_name = data.get('song_name')

    if musician:

        if password and song_name:
            response, status_code = delete_music(musician, password, song_name)
            return jsonify(response), status_code
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@musician_bp.route('/add_music', methods=['POST'])
@jwt_required()
def add_musics():
    musician = get_jwt_identity()
    data = request.json
    details = data.get('details')

    if musician:

        if details:
            response, status_code = add_music(musician, details)
            return jsonify(response), status_code
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401
    

@musician_bp.route('/delete_musician_details', methods=['DELETE'])
@jwt_required()        
def delete_musician_details():
    musician = get_jwt_identity()
    data = request.json
    password = data.get('password')

    if musician:

        if password:
            response, status_code = delete_musician(musician, password)
            return jsonify(response), status_code
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@musician_bp.route('/join_musician_room', methods=['POST'])
@jwt_required()
def join_chat_room():
    musician = get_jwt_identity()

    if musician:
        response = on_connect(musician, "redis_musician")

        if response['status'] == "success":
            return jsonify(response), 201
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@musician_bp.route('/send_message_musician', methods=['POST'])
@jwt_required()
def send_message():
    musician = get_jwt_identity()
    data = request.json
    room = data.get('room')
    message = data.get('message')

    if musician:
        response = handle_message(message, room, "musician")

        if response['status'] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401


@musician_bp.route('/leave_room_musician', methods=['POST'])
@jwt_required()
def delete_chat():
    musician = get_jwt_identity()

    if musician:
        response = handle_leave_room(musician, "user")

        if response['status'] == "success":
            return jsonify(response), 200
        
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401    


