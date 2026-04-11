# Iska use hota hai Python se MongoDB database ko connect aur control karne ke liye
# is mongo connection ko reuse krega bar bar islia alg file mai connection establish kr rha

from pymongo import MongoClient

# “Connect to MongoDB server named mongo on port 27017 using username admin and password admin”
# link : mongodb://username:password@servername(here its container name):port
mongo_client = MongoClient("mongodb://admin:admin@mongo:27017")
