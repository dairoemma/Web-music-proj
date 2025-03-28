from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request as flask_request

socket = None

def initialize_socket(app):
    global socket
    socket = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
    register_socket_events()
    return socket

def register_socket_events():
    @socket.on('connect')
    def handle_connect():
        print(f"Client connected: {flask_request.sid}")
        emit('connection_success', {'message': 'Connected to WebSocket'})

    @socket.on('join_room')
    def handle_join(data):
        username = data.get("username")
        if username:
            join_room(username)
            print(f"{username} joined room")
        else:
            emit('error', {'message': 'Username missing'})

    @socket.on('send_message')
    def handle_message(data):
        msg = data.get("message")
        room = data.get("room")  # recipient username
        sender = data.get("sender")

        if not msg or not room or not sender:
            emit('error', {'message': 'Missing message, room, or sender'})
            return

        emit('receive_message', {"sender": sender, "text": msg}, room=room)
        emit('receive_message', {"sender": sender, "text": msg}, room=sender)

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
