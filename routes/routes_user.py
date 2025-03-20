from flask import request, jsonify,Blueprint
from helper_function.jwt_initialization import create_token
from modules.user import get_all_user, get_user, insert_user, delete_user, update_user
from modules.musician import get_all_musician, get_musician, get_music, get_a_music
from helper_function.celery_file import process_payment
from datetime import datetime
from helper_function.redis_config import redis_user, redis_user_payment
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def index():
    return "Routes is running"


@user_bp.route('/payment_processed', methods=['POST'])
def payment_processed():
    data = request.json
    user_expiry_date = data['user_expiry_date']
   
   
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

    task = process_payment.apply_async(args=[account_name, account_number, cvv, password, expiry_date, amount_in_account])
    return jsonify({"message": "payment processing started", "task_id": task.id}), 202


@user_bp.route('/payment_status/<task_id>', methods=['GET'])
def payment_status(task_id):

    task = process_payment.AsyncResult(task_id)

    if task.state == "PENDING":
        return jsonify({"STATUS": "processing payment"}), 202
    
    elif task.state == "SUCCESS":

        redis_user_payment.setex(f"task_id:{task_id}", 3600, "verified")
        return jsonify({"STATUS": f"payment processes, task id is:{task_id}. Don't forget to copy task_id"}), 200
    
    else:
        return jsonify({"STATUS": task.state}), 400
    


@user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    data =  request.json
    task_id = data.get('task_id')

    if not task_id:

        return jsonify({"status": "error", "message": "Task ID is required"}), 400
    
    if redis_user_payment.get(f"task_id:{task_id}") == "verified":

        response, status_code = insert_user(data)
        return jsonify (response), status_code
    
    else:
        return jsonify ({"status": "error", "message": "Invalid Task ID. Complete payment first"}), 400


@user_bp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user_details = get_user(username)

        if check_password_hash(user_details['password'], password):
            access_token = create_token(id=username)
            return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200
        else:
            return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401    
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

@user_bp.route('/user_profile', methods=['GET'])
@jwt_required
def user_profile():
    user = get_jwt_identity()

    if user:
        user_details = get_user(user)
        return jsonify(user_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access Denied"}), 401
    
    
@user_bp.route('/search_user', methods=['GET'])
@jwt_required
def search_user():
    data = request.json
    user_to_search = data.get('user_to_search')
    user = get_jwt_identity()

    if user:
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


@user_bp.route('/get_users', methods=['GET'])
@jwt_required
def get_user():
    user = get_jwt_identity()

    if user:
        users_details = get_all_user()
        return jsonify(users_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@user_bp.route('/search_musician', methods=['GET'])
@jwt_required
def search_musician():
    user = get_jwt_identity()
    data = request.json
    musician = data.get('musician')

    if user:
        if musician:
            musician_details = get_musician(musician)
            if musician_details:
                return jsonify(musician_details), 200
            else:
                return jsonify({"status": "error", "message": "Musician not found"}), 404
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401    


@user_bp.route('/get_musicians', methods=['GET'])
@jwt_required
def get_musicians():
    user = get_jwt_identity()

    if user:
        musicians_details = get_all_musician()
        return jsonify(musicians_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401
    

@user_bp.route('/search_music', methods=['GET'])
@jwt_required
def search_music():
    data = request.json
    music_details = data.get('music_details')
    user = get_jwt_identity()

    if user:
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
@jwt_required
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
@jwt_required
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
@jwt_required        
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


