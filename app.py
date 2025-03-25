from flask import Flask
from config import Config
from helper_function.jwt_initialization import initialize_jwt
from helper_function.celery_file import make_celery
from routes import blueprints
from helper_function.socket_file import initialize_socket


app = Flask(__name__)

app.config.from_object(Config)

jwt = initialize_jwt(app=app)

for bp in blueprints:
    app.register_blueprint(bp)

celery = make_celery(app)

socket = initialize_socket(app=app)

if __name__ == '__main__':
   socket.run(app, host="0.0.0.0", port=5000, debug=True)




