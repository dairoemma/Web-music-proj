import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URI = os.getenv('MONGO_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    Cloud_name = os.getenv('CLOUD_NAME')
    Api_key = os.getenv('API_KEY')
    Api_secret = os.getenv('API_SECRET')
    