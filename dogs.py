# POST = request.args, use params
# PUT = request.forms
# GET = request.args, use params
#

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

@app.route('/dogs/api/v1/createdog', methods=["POST"])
def create():
	print("FUNCTION: CREATE/PUT")
	data = request.args
	sd_name = data['sd_name']
	sd_regstatus = data['sd_regstatus']
	sd_teamstatus = data['sd_teamstatus']
	sd_vaccstatus = data['sd_vaccstatus']
	sd_vaccexpiredate = data['sd_vaccexpiredate']
	sd_pedigree = data['sd_pedigree']
	sd_regid = data['sd_regid']

	dog_present = dogs_collection.find_one({"sd_regid": sd_regid}, {'sd_name': 1})
	print(dog_present, sd_regid)
	if not dog_present:
		dogs_collection.insert_one({'sd_regid': sd_regid,
									'sd_name': sd_name,
									'sd_regstatus': sd_regstatus,
									'sd_teamstatus': sd_teamstatus,
									'sd_vaccstatus': sd_vaccstatus,
									'sd_vaccexpiredate': sd_vaccexpiredate,
									'sd_pedigree': sd_pedigree})
		response = {'status': "Dog added to database.", 'code': 100}
	else:
		response = {'status': "Dog already in database, not added.", 'code': 101}

	return jsonify(response)

@app.route('/dogs/api/v1/readdog/', methods=["GET"])
def read():
	print("FUNCTION: READ/GET")
	req = request.args  # Put all passed parameters in a dictionary
	sd_regid = str(req['sd_regid'])
	dog_details = dogs_collection.find_one({'sd_regid': sd_regid}, {'sd_regid': 1,'sd_name': 1,'sd_regstatus': 1,
														   'sd_teamstatus': 1,'sd_vaccstatus': 1,'sd_vaccexpiredate':
															   1,'sd_pedigree': 1})
	print(sd_regid, "dog_details:",dog_details)

	if dog_details:
		print("in_dog_details")
		sd_regid = int(dog_details['sd_regid'])
		sd_name = dog_details['sd_name']
		sd_regstatus =  dog_details['sd_regstatus']
		sd_teamstatus = dog_details['sd_teamstatus']
		sd_vaccstatus = dog_details['sd_vaccstatus']
		sd_vaccexpiredate = dog_details['sd_vaccexpiredate']
		sd_pedigree = dog_details['sd_pedigree']

		dog = {'sd_regid': sd_regid,
			   'sd_name': sd_name,
			   'sd_regstatus': sd_regstatus,
			   'sd_teamstatus': sd_teamstatus,
			   'sd_vaccstatus': sd_vaccstatus,
			   'sd_vaccexpiredate': sd_vaccexpiredate,
			   'sd_pedigre': sd_pedigree}
		response = dog
	else:
		response = {'status': "Dog not found in database.", 'code': 101}

	return jsonify(response)

@app.route('/dogs/api/v1/updatedogs/regstatus/', methods=["PUT"])
def update_regstatus():
	print("FUNCTION: UPDATE_REGSTATUS/PUT")
	data = request.form
	sd_regstatus = data['sd_regstatus']
	sd_regid = data['sd_regid']
	dog_details = dogs_collection.find_one({'sd_regid': sd_regid}, {'sd_regid': 1, 'sd_name': 1, 'sd_regstatus': 1,
																	'sd_teamstatus': 1, 'sd_vaccstatus': 1,
																	'sd_vaccexpiredate':
																		1, 'sd_pedigree': 1})
	if dog_details:
		dogs_collection.find_one_and_replace({"sd_regid": sd_regid}, {'sd_name': dog_details['sd_name'],
																	  "sd_regid": sd_regid,
																	  "sd_teamstatus": dog_details['sd_teamstatus'],
																	  "sd_vaccstatus":dog_details['sd_vaccstatus'],
																	  "sd_vaccexpiredate":dog_details['sd_vaccexpiredate'],
																	  "sd_pedigree":dog_details['sd_pedigree'],
																	  "sd_regstatus":sd_regstatus})
		# dogs_collection.insert_one({'sd_regid': sd_regid,
		# 							'sd_name': sd_name,
		# 							'sd_regstatus': sd_regstatus,
		# 							'sd_teamstatus': sd_teamstatus,
		# 							'sd_vaccstatus': sd_vaccstatus,
		# 							'sd_vaccexpiredate': sd_vaccexpiredate,
		# 							'sd_pedigree': sd_pedigree})
		response = {'status': "Dog registration status updated.", 'code': 100}
	else:
		response = {'status': "Dog not in database.", 'code': 101}

	return jsonify(response)

@app.route('/dogs/api/v1/updatedogs/teamstatus/', methods=["PUT"])
def update_teamstatus():
	print("FUNCTION: UPDATE_TEAMSTATUS/PUT")
	data = request.form
	sd_teamstatus = data['sd_teamstatus']
	sd_regid = data['sd_regid']
	dog_details = dogs_collection.find_one({'sd_regid': sd_regid}, {'sd_regid': 1, 'sd_name': 1, 'sd_regstatus': 1,
																	'sd_teamstatus': 1, 'sd_vaccstatus': 1,
																	'sd_vaccexpiredate':
																		1, 'sd_pedigree': 1})
	if dog_details:
		dogs_collection.find_one_and_replace({"sd_regid": sd_regid}, {'sd_name': dog_details['sd_name'],
																	  "sd_regid": sd_regid,
																	  "sd_teamstatus": sd_teamstatus,
																	  "sd_vaccstatus":dog_details['sd_vaccstatus'],
																	  "sd_vaccexpiredate":dog_details['sd_vaccexpiredate'],
																	  "sd_pedigree":dog_details['sd_pedigree'],
																	  "sd_regstatus":dog_details['sd_regstatus']})
		# dogs_collection.insert_one({'sd_regid': sd_regid,
		# 							'sd_name': sd_name,
		# 							'sd_regstatus': sd_regstatus,
		# 							'sd_teamstatus': sd_teamstatus,
		# 							'sd_vaccstatus': sd_vaccstatus,
		# 							'sd_vaccexpiredate': sd_vaccexpiredate,
		# 							'sd_pedigree': sd_pedigree})
		response = {'status': "Dog team status updated.", 'code': 100}
	else:
		response = {'status': "Dog not in database.", 'code': 101}

	return jsonify(response)

@app.route('/dogs/api/v1/updatedogs/sd_vaccexpiredate/', methods=["PUT"])
def update_vaccexpiredate():
	print("FUNCTION: UPDATE_VACEXPIREDATA/PUT")
	data = request.form
	sd_vaccexpiredate = data['sd_vaccexpiredate']
	sd_regid = data['sd_regid']
	dog_details = dogs_collection.find_one({'sd_regid': sd_regid}, {'sd_regid': 1, 'sd_name': 1, 'sd_regstatus': 1,
																	'sd_teamstatus': 1, 'sd_vaccstatus': 1,
																	'sd_vaccexpiredate':
																		1, 'sd_pedigree': 1})
	if dog_details:
		dogs_collection.find_one_and_replace({"sd_regid": sd_regid}, {'sd_name': dog_details['sd_name'],
																	  "sd_regid": sd_regid,
																	  "sd_teamstatus": dog_details['sd_teamstatus'],
																	  "sd_vaccstatus":dog_details['sd_vaccstatus'],
																	  "sd_vaccexpiredate":sd_vaccexpiredate,
																	  "sd_pedigree":dog_details['sd_pedigree'],
																	  "sd_regstatus":dog_details['sd_regstatus']})
		# dogs_collection.insert_one({'sd_regid': sd_regid,
		# 							'sd_name': sd_name,
		# 							'sd_regstatus': sd_regstatus,
		# 							'sd_teamstatus': sd_teamstatus,
		# 							'sd_vaccstatus': sd_vaccstatus,
		# 							'sd_vaccexpiredate': sd_vaccexpiredate,
		# 							'sd_pedigree': sd_pedigree})
		response = {'status': "Dog vaccination expiry data updated.", 'code': 100}
	else:
		response = {'status': "Dog not in database.", 'code': 101}

	return jsonify(response)

if __name__ == "__main__":
	app.run(debug=False, host='127.0.0.1', port=int(os.getenv('PORT', '5000')))