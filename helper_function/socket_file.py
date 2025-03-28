from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request as flask_request
from helper_function.redis_config import redis_client

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
        redis_client.set(f"{role}_room:{user_id}", role)
        emit('joined_room', {'message': f"{user_id} joined room", "room": user_id}, room=user_id)

    @socket.on('get_active_rooms')
    def handle_get_active_rooms():
        keys = redis_client.keys("*_room:*")
        users = [{"username": k.split(":")[1], "role": k.split(":")[0]} for k in keys]
        emit('active_rooms', users)

    @socket.on('send_message')
    def handle_message(data):
        msg = data.get("message")
        room = data.get("room")

        if not msg or not room:
            emit('error', {'message': 'Message or room missing'})
            return

        emit('receive_message', msg, room=room)

    @socket.on('leave_room')
    def handle_leave(data):
        room = data.get("room")
        role = data.get("role")

        if not room or not role:
            emit('error', {'message': 'Missing room or role'})
            return

        leave_room(room)
        redis_client.delete(f"{role}_room:{room}")
        emit('left_room', {'message': f"Left room {room}"})