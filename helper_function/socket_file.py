from flask_socketio import SocketIO #emit, join_room, leave_room
# from flask import request as flask_request


# important comment
#  we wanted to implement a chatroom using the flask_socketio for rtc but it didn't work, we used redis at first to store the rooms but redis failed
#  we then used the username but there was no rtc, due to deadline drawing near, we couldn't delete the socket code because we used it to run the app.py and we used eventlet in our docker
#  so the socket initialization is the only code we left uncommented because of that reason


socket = None
# active_users = {}

def initialize_socket(app):
    global socket
    socket = SocketIO(app, cors_allowed_origins="*")
    return socket

# def register_socket_events():
#     @socket.on('connect')
#     def handle_connect():
#         print(f"Client connected: {flask_request.sid}")
#         emit('connection_success', {'message': 'Connected to WebSocket'})

#     @socket.on('join_room')
#     def handle_join(data):
#         username = data.get("username")
#         if not username:
#             emit('error', {'message': 'Missing username'})
#             return
#         join_room(username)
#         active_users[flask_request.sid] = username
#         print(f"{username} joined room")
#         emit('joined_room', {'message': f"{username} joined"}, room=username)

#     @socket.on('send_message')
#     def handle_send_message(data):
#         msg = data.get("message")
#         room = data.get("room")
#         if not msg or not room:
#             emit('error', {'message': 'Missing message or room'})
#             return
#         emit('receive_message', msg, room=room)

#     @socket.on('disconnect')
#     def handle_disconnect():
#         sid = flask_request.sid
#         username = active_users.pop(sid, None)
#         print(f"Client disconnected: {sid} ({username})")

#     @socket.on('leave_room')
#     def handle_leave(data):
#         room = data.get("room")
#         if room:
#             leave_room(room)
#             emit('left_room', {'message': f"Left room {room}"})
