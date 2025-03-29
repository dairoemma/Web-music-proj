from flask_jwt_extended import  JWTManager, create_access_token #import jwt dependencies


#  initialize the jwt
def initialize_jwt(app):
   jwt = JWTManager(app)
   return jwt
# function to generate token
def create_token(id):
   return create_access_token(identity=id) #returns the creted access token with the identity being the username or artist name which is unique






    

