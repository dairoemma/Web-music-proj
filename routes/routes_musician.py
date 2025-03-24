from flask import Flask, request, jsonify, Blueprint
from helper_function.jwt_initialization import create_token
from modules.musician import  get_musician, insert_musician, delete_musician, update_music, update_musician, add_music
from datetime import datetime
from helper_function.celery_file import process_payment
from helper_function.redis_config import redis_musician, redis_musician_payment
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

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

    task = process_payment.apply_async(args=[account_name, account_number, cvv, password, expiry_date, amount_in_account])
    return jsonify({"message": "payment processing started", "task_id": task.id}), 202


@musician_bp.route('/payment_status/<task_id>', methods=['GET'])
def payment_status(task_id):

    task = process_payment.AsyncResult(task_id)

    if task.state == "PENDING":
        return jsonify({"STATUS": "processing payment"}), 202
    
    elif task.state == "SUCCESS":

        redis_musician_payment.setex(f"task_id:{task_id}", 3600, "verified")
        return jsonify({"STATUS": f"payment processes, task id is:{task_id}. Don't forget to copy task_id"}), 200
    
    else:
        return jsonify({"STATUS": task.state}), 400
    


@musician_bp.route('/add_musician', methods=['GET', 'POST'])
def add_musician():
    data =  request.json
    task_id = data.get('task_id')

    if not task_id:

        return jsonify({"status": "error", "message": "Task ID is required"}), 400
    
    if redis_musician_payment.get(f"task_id:{task_id}") == "verified":

        response, status_code = insert_musician(data)
        return jsonify (response), status_code
    
    else:
        return jsonify ({"status": "error", "message": "Invalid Task ID. Complete payment first"}), 400


@musician_bp.route('/authenticate_musician', methods=['POST'])
def authenticate_musician():
    data = request.json
    music_name = data.get('music_name')
    password = data.get('password')

    if music_name and password:
        musician_details = get_musician(username=music_name)

        if check_password_hash(musician_details['password'], password):
            access_token = create_token(id=music_name)
            return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200
        else:
            return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401    
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
def search_user():
    data = request.json
    user_to_search = data.get('user_to_search')
    musician = get_jwt_identity()

    if musician:
        if user_to_search:
            user_details = get_user(user_to_search)
            if user_details:
                return jsonify(user_details), 200
            else:
                return jsonify({"status": "error","message": "User not found"}), 404
        else:
            return jsonify({"status": "error", "message": "All fieds required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401 


@musician_bp.route('/get_users', methods=['GET'])
@jwt_required()
def get_user():
    musician = get_jwt_identity()

    if musician:
        users_details = get_all_user()
        return jsonify(users_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@musician_bp.route('/search_musician', methods=['GET'])
@jwt_required()
def search_musician():
    musician = get_jwt_identity()
    data = request.json
    musician_name = data.get('musician')

    if musician:
        if musician_name:
            musician_details = get_musician(musician)
            if musician_details:
                return jsonify(musician_details), 200
            else:
                return jsonify({"status": "error", "message": "Musician not found"}), 404
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401    


@musician_bp.route('/get_musicians', methods=['GET'])
@jwt_required()
def get_musicians():
    user = get_jwt_identity()

    if user:
        musicians_details = get_all_musician()
        return jsonify(musicians_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401
    

@musician_bp.route('/search_music', methods=['GET'])
@jwt_required()
def search_music():
    data = request.json
    music_details = data.get('music_details')
    musician = get_jwt_identity()

    if musician:
        if music_details:
            music = get_a_music(music_details)
            if music:
                return jsonify(music), 200
            else:
                return jsonify({"status": "error", "message": "Music not found"}), 404
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401    


@user_bp.route('/get_musician_catalogue', methods=['GET'])
@jwt_required()
def get_musician_catalogue():
    data = request.json
    user = get_jwt_identity()
    musician_name = data.get('musician_name')

    if user:
        if musician_name:
            music_details = get_music(musician_name)
            if music_details:
                return jsonify(music_details), 200
            else:
                return jsonify({"status": "error", "message": "Musician not found"}), 404
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400    
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401
    

@user_bp.route('/update_user_info', methods=['PUT'])
@jwt_required()
def update_user_info():
    user = get_jwt_identity()
    data = request.json
    details = data.get('details')

    if user:
        if details:
            response, status_code = update_user(user, details)
            return jsonify(response), status_code
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@user_bp.route('/delete_user_details', methods=['DELETE'])
@jwt_required()        
def delete_user_details():
    user = get_jwt_identity()
    data = request.json
    password = data.get('password')

    if user:
        if password:
            response, status_code = delete_user(user, password)
            return jsonify(response), status_code
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@user_bp.route('/join_user_room', methods=['POST'])
@jwt_required()
def join_chat_room():
    user = get_jwt_identity()

    if user:
        response = on_connect(user, "redis_user")

        if response['status'] == "success":
            return jsonify(response), 201
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@user_bp.route('/send_message_user', methods=['POST'])
@jwt_required()
def send_message():
    user = get_jwt_identity()
    data = request.json
    room = data.get('room')
    message = data.get('message')

    if user:
        response = handle_message(message, room, "user")

        if response['status'] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401


@user_bp.route('/leave_room_user', methods=['POST'])
@jwt_required()
def delete_chat():
    user = get_jwt_identity()

    if user:
        response = handle_leave_room(user, "user")

        if response['status'] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401    


