from pymongo import MongoClient
from config import Config
# initialize the mongodb
client = MongoClient(Config.DATABASE_URI)

# initialize the database
db = client['Quackathon_uni-database']

# initialize the collections
users_collection = db['User']
musicians_collection = db['Musician']
admins_collection = db['Admin']