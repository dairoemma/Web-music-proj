from flask_jwt_extended import  JWTManager, create_access_token, get_jwt_identity
from flask import request


def initialize_jwt(app):
   jwt = JWTManager(app)
   return jwt

def create_token(id):
   return create_access_token(identity=id)






    

