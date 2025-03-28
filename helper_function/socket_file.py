from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request as flask_request

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

    @socket.on('send_message')
    def handle_message(data):
        msg = data.get("message")
        room = data.get("room")

        if not msg or not room:
            emit('error', {'message': 'Missing message or room'})
            return

        # Broadcast to the recipient room
        emit('receive_message', msg, room=room)

    @socket.on('disconnect')
    def handle_disconnect():
        print(f"Client disconnected: {flask_request.sid}")

    @socket.on('leave_room')
    def handle_leave(data):
        room = data.get("room")
        if not room:
            emit('error', {'message': 'Missing room'})
            return
        leave_room(room)
        emit('left_room', {'message': f"Left room {room}"})
