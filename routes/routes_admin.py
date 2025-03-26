from flask import request, jsonify, Blueprint
from helper_function.jwt_initialization import create_token
from modules.admin import get_admin, get_all_admin, insert_admin, delete_admin, update_admin
from helper_function.utility import search_music, search_musician, search_user, get_musician_catalogue, get_all_users, get_musicians
from modules.user import delete_user
from modules.musician import delete_musician
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper_function.socket_file import handle_message, handle_leave_room, on_connect


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
    return "admin routes is running"


@admin_bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    data =  request.json

    response, status_code = insert_admin(data)
    return jsonify (response), status_code


@admin_bp.route('/authenticate_admin', methods=['POST'])
def authenticate_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        admin_details = get_admin(username)

        if check_password_hash(admin_details['password'], password):
            access_token = create_token(id=username)
            return jsonify({"status": "success", "message": "Access Granted", "access_token": access_token}), 200
        else:
            return jsonify({"status": "error", "message": "Access Denied, Invalid Credentials"}), 401    
    else:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    

@admin_bp.route('/admin_profile', methods=['GET'])
@jwt_required()
def admin_profile():
    admin = get_jwt_identity()

    if admin:
        admin_details = get_admin(admin)
        return jsonify(admin_details), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access Denied"}), 401
    

@admin_bp.route('/get_all_admin', methods=['GET'])
@jwt_required()
def get_all_admins():
    admin = get_jwt_identity()
    
    if admin:
        admin_list = get_all_admin()
        return jsonify(admin_list), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credential, Access denied"}), 401


@admin_bp.route('/search_user', methods=['GET'])
@jwt_required()
def search_a_user():
    data = request.json
    user_to_search = data.get('user_to_search')
    user = get_jwt_identity()

    response, status_code = search_user(user, user_to_search)
    return jsonify(response), status_code


@admin_bp.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    admin = get_jwt_identity()

    response, status_code = get_all_users(admin)
    return jsonify(response), status_code


@admin_bp.route('/search_musician', methods=['GET'])
@jwt_required()
def search_a_musician():
    admin = get_jwt_identity()
    data = request.json
    musician_name = data.get('musician')

    response, status_code =  search_musician(admin, musician_name)
    return jsonify(response), status_code


@admin_bp.route('/get_musicians', methods=['GET'])
@jwt_required()
def get_all_musicians():
    admin = get_jwt_identity()
    
    response, status_code = get_musicians(admin)
    return jsonify(response), status_code


@admin_bp.route('/search_music', methods=['GET'])
@jwt_required()
def search_a_music():
    data = request.json
    music_details = data.get('music_details')
    admin = get_jwt_identity()

    response, status_code = search_music(admin, music_details)
    return jsonify(response), status_code  


@admin_bp.route('/get_musician_catalogue', methods=['GET'])
@jwt_required()
def get_musician_catalogue():
    data = request.json
    admin = get_jwt_identity()
    musician_name = data.get('musician_name')

    response, status_code = get_musician_catalogue(admin, musician_name)
    return jsonify(response), status_code
    

@admin_bp.route('/update_admin_info', methods=['PUT'])
@jwt_required()
def update_admin_info():
    admin = get_jwt_identity()
    data = request.json
    details = data.get('details')

    if admin:
        if details:
            response, status_code = update_admin(admin, details)
            return jsonify(response), status_code
        else:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@admin_bp.route('/delete_user_details', methods=['DELETE'])
@jwt_required()        
def delete_user_details():
    admin  = get_jwt_identity()
    data = request.json
    password = data.get('password')
    user_to_delete = data.get('user_to_delete')
    admin_details = get_admin(admin) 

    if admin_details:
        if check_password_hash(admin_details['password'], password):
            result = search_user(admin, user_to_delete)
            response, status_code = delete_user(user_to_delete, result['password'])
            return jsonify(response), status_code
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@admin_bp.route('/delete_musician_details', methods=['DELETE'])
@jwt_required()        
def delete_musician_details():
    admin  = get_jwt_identity()
    data = request.json
    password = data.get('password')
    musician_to_delete = data.get('user_to_delete')
    admin_details = get_admin(admin) 

    if admin_details:
        if check_password_hash(admin_details['password'], password):
            result = search_musician(admin, musician_to_delete)
            response, status_code = delete_musician(musician_to_delete, result['password'])
            return jsonify(response), status_code
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401
    

@admin_bp.route('/delete_admin_details', methods=['DELETE'])
@jwt_required()        
def delete_admin_details():
    admin = get_jwt_identity()
    data = request.json
    password = data.get('password')

    if admin:
        if password:
            response, status_code = delete_admin(admin, password)
            return jsonify(response), status_code
        else:
            return jsonify({"status":"error", "message": "All fields are required"}), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@admin_bp.route('/join_admin_room', methods=['POST'])
@jwt_required()
def join_chat_room():
    admin = get_jwt_identity()

    if admin:
        response = on_connect(admin, "redis_user")

        if response['status'] == "success":
            return jsonify(response), 201
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, Access denied"}), 401


@admin_bp.route('/send_message_admin', methods=['POST'])
@jwt_required()
def send_message():
    admin = get_jwt_identity()
    data = request.json
    room = data.get('room')
    message = data.get('message')

    if admin:
        response = handle_message(message, room, "admin")

        if response['status'] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401


@admin_bp.route('/leave_room_admin', methods=['POST'])
@jwt_required()
def delete_chat():
    admin = get_jwt_identity()

    if admin:
        response = handle_leave_room(admin, "admin")

        if response['status'] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400
        
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials, Access denied"}), 401    


