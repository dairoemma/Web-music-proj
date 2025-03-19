from socketio import SocketIO


def initialize_socket(app):
    socket =  SocketIO(app, cors_allowed_origin="*")
    return socket


