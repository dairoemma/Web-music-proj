from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request as flask_request
from helper_function.redis_config import redis_user, redis_admin, redis_musician


socket = None


def initialize_socket(app):
    global socket
    socket = SocketIO(app, cors_allowed_origins="*")
    register_socket_events()
    return socket


def register_socket_events():
    @socket.on('connect')
    def handle_connect():
        print(f"Client connected: {flask_request.sid}")
        emit('connection_success', {'message': 'Connected to WebSocket'})


    @socket.on('join_room')
    def handle_join(data):
        user_id = data.get("id")
        role = data.get("role")

        if not user_id or not role:
            emit('error', {'message': 'Missing ID or role'})
            return

        join_room(user_id)

        if role == "user":
            redis_user.set(f"user_room{user_id}", user_id)
        elif role == "musician":
            redis_musician.set(f"musician_room{user_id}", user_id)
        elif role == "admin":
            redis_admin.set(f"admin_room{user_id}", user_id)
        else:
            emit('error', {'message': 'Invalid role'})
            return

        emit('joined_room', {'message': f"{user_id} joined room", "room": user_id}, room=user_id)


    @socket.on('send_message')
    def handle_message(data):
        msg = data.get("message")
        room = data.get("room")
        role = data.get("role")

        if not msg or not room or not role:
            emit('error', {'message': 'Message, room, or role missing'})
            return

        if role == "user" and redis_user.get(f"user_room{room}"):
            emit('receive_message', msg, room=room)
        elif role == "musician" and redis_musician.get(f"musician_room{room}"):
            emit('receive_message', msg, room=room)
        elif role == "admin" and redis_admin.get(f"admin_room{room}"):
            emit('receive_message', msg, room=room)
        else:
            emit('error', {'message': 'Invalid room or role'})


    @socket.on('leave_room')
    def handle_leave(data):
        room = data.get("room")
        role = data.get("role")

        if not room or not role:
            emit('error', {'message': 'Missing room or role'})
            return

        leave_room(room)

        if role == "user":
            redis_user.delete(f"user_room{room}")
        elif role == "musician":
            redis_musician.delete(f"musician_room{room}")
        elif role == "admin":
            redis_admin.delete(f"admin_room{room}")
        else:
            emit('error', {'message': 'Invalid role'})
            return

        emit('left_room', {'message': f"Left room {room}"})
