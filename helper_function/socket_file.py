from socketio import SocketIO, emit, join_room, leave_room
from helper_function.redis_config import redis_user, redis_admin, redis_musician


def initialize_socket(app):
    socket =  SocketIO(app, cors_allowed_origin="*")
    return socket


@socket.on('connect')
def on_connect(id, redis_type):
    if id:
        room = join_room(id)
        if redis_type == "redis_user":
            redis_user.set(f"user_room{room}", room)
            return "success"
        elif redis_type == "redis_musician":
            redis_musician.set(f"muician_room{room}", room) 
            return "success"
        elif redis_type == "redis_admin":
            redis_admin.set(f"admin_room{room}", room)
            return "success"
        else:
            return "redis_type not found"
    else:
        return "id missing"


@socket.on('message')
def handle_message(msg, room, role):
    if msg and room:
        if role == "user":
            validate_user_room = redis_user.get(room)
            if validate_user_room:
                emit(msg, to=room)
            else:
                return "couldn't find user room"
        elif role == "musician":
            validate_musician_room = redis_musician.get(room)
            if validate_musician_room:
                emit(msg, to=room)
            else:
                return "couldn't find musician room"
        elif role == "admin":
            validate_admin_room = redis_admin.get(room)
            if validate_admin_room:
                emit(msg, to=room) 
        else:
            return "role doesn't exist"
    else:
        return "couldn't send message, message and room missing" 


@socket.on('leave_room')    
def handle_leave_room(room, role):
    if room and role:
      if role == "user":
        leave_room(room)
        redis_user.delete(room)
        return "successfully deleted user chat"
      elif role == "musician":
        leave_room(room)
        redis_musician.delete(room)
        return "successfully deleted musician chat"
      elif role == "admin": 
        leave_room(room)
        redis_admin.delete(room)
        return "successfully deleted admin chat"
      else:
          return "role doesn't exist"
    else:
        return "couldn't send message, message and room missing"
      