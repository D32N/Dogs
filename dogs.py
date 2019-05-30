from flask import Flask, jsonify, request
import os, json
import pymongo

app = Flask(__name__)
## connect to the mongo database
print "\n## Establish the connection and aim at a specific database"
if 'VCAP_SERVICES' in os.environ:
	VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
	MONCRED = VCAP_SERVICES["mlab"][0]["credentials"]
	client = pymongo.MongoClient(MONCRED["uri"])
	DB_NAME = str(MONCRED["uri"].split("/")[-1])
else:
	client = pymongo.MongoClient('127.0.0.1:27017')
	DB_NAME = "DogsDB"

print "Connecting to database : " + DB_NAME

## connect database if it exists, or create database
dogs_db = client[DB_NAME]
COL_NAME = "dogs_details"
dogs_collection = dogs_db[COL_NAME]



@app.route('/dogs/', method=["PUT"])
def create():

	response = {'status' : "ok"}
	return jsonify(response)

if __name__ == "__main__":
	app.run(debug=False, host='127.0.0.1', port=int(os.getenv('PORT', '5000')))