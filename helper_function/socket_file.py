from flask_socketio import SocketIO, emit, join_room, leave_room
from helper_function.redis_config import redis_user, redis_admin, redis_musician


socket = None


def initialize_socket(app):
    global socket
    socket =  SocketIO(app, cors_allowed_origin="*")
    return socket



def on_connect(id, redis_type):
    if id:
        room = join_room(id)
        if redis_type == "redis_user":
            redis_user.set(f"user_room{room}", room)
            return {"status": "success", "message": f"{id} created chat room {room}"}
        elif redis_type == "redis_musician":
            redis_musician.set(f"muician_room{room}", room) 
            return {"status": "success", "message": f"{id} created chat room {room}"}
        elif redis_type == "redis_admin":
            redis_admin.set(f"admin_room{room}", room)
            return {"status": "success", "message": f"{id} created chat room {room}"}
        else:
            return {"status": "error", "message": "redis_type not found"}
    else:
        return {"status": "error", "message": "id missing"}


def handle_message(msg, room, role):
    if msg and room:
        if role == "user":
            validate_user_room = redis_user.get(room)
            if validate_user_room:
                emit(msg, to=room)
                return {"status": "success", "message": f"message sent"}
            else:
                return {"status": "error", "message": "couldn't find user chat"}
        elif role == "musician":
            validate_musician_room = redis_musician.get(room)
            if validate_musician_room:
                emit(msg, to=room)
                return {"status": "success", "message": f"message sent"}
            else:
                return {"status": "error", "message": "couldn't find musician chat"}
        elif role == "admin":
            validate_admin_room = redis_admin.get(room)
            if validate_admin_room:
                emit(msg, to=room) 
                return {"status": "success", "message": f"message sent"}
            else:
                return {"status": "error", "message": "couldn't find admin chat"}
        else:
            return {"status": "error", "message": "role doesn't exist"}
    else:
        return {"status": "error", "message": "couldn't send message, message and chat_room missing"}


   
def handle_leave_room(room, role):
    if room and role:
      if role == "user":
        leave_room(room)
        redis_user.delete(room)
        return {"status": "error", "message": "successfully deleted user chat"}
      elif role == "musician":
        leave_room(room)
        redis_musician.delete(room)
        return {"status": "error", "message": "successfully deleted musician chat"}
      elif role == "admin": 
        leave_room(room)
        redis_admin.delete(room)
        return {"status": "error", "message": "successfully deleted admin chat"}
      else:
          return {"status": "error", "message": "role doesn't exist"}
    else:
        return {"status": "error", "message": "couldn't send message, room and role missing"}
    
      