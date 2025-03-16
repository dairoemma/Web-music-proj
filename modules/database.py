from pymongo import MongoClient
from config import Config

client = MongoClient(Config.DATABASE_URI)

db = client['Quackathon_uni-database']

users_collection = db['User']
musicians_collection = db['Musician']
admins_collection = db['Admin']