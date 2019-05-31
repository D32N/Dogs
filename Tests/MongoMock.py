from pymongo import MongoClient

monog_url = 'mongodb://localhost:27017'
client = MongoClient(monog_url)
db = client.db