import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URI = os.getenv('MONGO_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    Cloud_name = os.getenv('CLOUD_NAME')
    Api_key = os.getenv('API_KEY')
    Api_secret = os.getenv('API_SECRET')
    REDIS_URL = os.getenv('REDIS_URL')
    # REDIS_USER_DB = os.getenv('REDIS_USER_DB')
    # REDIS_MUSICIAN_DB = os.getenv('REDIS_MUSICIAN_DB')
    # REDIS_ADMIN_DB = os.getenv('REDIS_ADMIN_DB')
    # REDIS_USER_PAYMENT_DB = os.getenv('REDIS_USER_PAYMENT_DB')
    # REDIS_MUSICIAN_PAYMENT_DB = os.getenv('REDIS_MUSICIAN_PAYMENT_DB')
    # CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    # CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')

    