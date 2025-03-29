from flask import Flask
from config import Config
from helper_function.jwt_initialization import initialize_jwt
# from helper_function.celery_file import make_celery
from routes import blueprints
from helper_function.socket_file import initialize_socket
from flask_cors import CORS

#initialize the flask app
app = Flask(__name__)

CORS(app) #initialize cors
app.config.from_object(Config) # configure Config

jwt = initialize_jwt(app=app)# initialize jwt

for bp, prefix in blueprints:
    app.register_blueprint(bp, url_prefix=prefix) #rigister the blueprints

# celery = make_celery(app)

socket = initialize_socket(app=app) #initialize the socket 

# run the app.py
if __name__ == '__main__':
   socket.run(app, host="0.0.0.0", port=5000, debug=True)




