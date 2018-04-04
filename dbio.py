#read out or insert in content in database
#Teng++

import pymongo
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.apps import custom_app_context as pwd_context
from beaker.middleware import SessionMiddleware


class Dbio:
	def __init__(self):
		client = MongoClient('45.32.65.58',27017)
		db = client.accenture_t1	#name of the database is "accenture_t1"

		#There is a collection called "alpha" in my database, so I need to get it...
		self.alpha = db.alpha
		self.proc = db.processes
		self.authentication = db.authentication
		self.malware = db.malware
		self.average_proctime = db.avptime
		self.counter_newmw = db.newmw
		print("\n CONNECT DB SUCCESS! \n")




	def db_insert_to_login(self, username, password):	#Insert username and password into the database
		sample = {"Username":username, "pwdhash":password}
		self.authentication.insert(sample)

	def db_get_user_by_username(self, username):
		return self.authentication.find({'Username': username})


	def db_verify_login(self, username):
		user_object = db_get_user_by_username(username)
		username = user_object["Username"]
		password = user_object["pwdhash"]


	def db_insert_to(self, name, md5, sha256):	#Insert a piece of information into the database
		sample = {"Name":name, "MD5":md5, "SHA256":sha256}
		self.alpha.insert(sample)

	def db_get_count(self):	#Get how many items are there in the database
		return self.alpha.find().count()

	def db_list_one(self, name,val): #Show one result using specific rule
		return self.alpha.find_one({name:val})

	def db_find_by_id(self, id):
		return self.alpha.find_one({"_id":ObjectId(id)})

	def db_gui_insert_newmw(self):
		info = {"NTime":time.time()}
		self.counter_newmw.insert(info)

	def db_gui_get_newmw(self):
		return self.counter_newmw.find({},{'NTime':1,'_id':0})

	def db_list_all_time(self):
		for i in self.alpha.find({},{'time':1,'_id':0}):
			print(i)

	def db_add_malware(self,time):
		info = {"Time":time}
		self.malware.insert(info)

	def db_add_avgtime(self,time):
		info = {"ATime":time}
		self.average_proctime.insert(info)

	def db_list_avgproctime(self):
		return self.average_proctime.find({},{'ATime':1,'_id':0})

	def db_list_malwaredate(self):
		return self.malware.find({},{'Time':1,'_id':0})
	# increments the amount of times a file has been run
	def db_inc_runs_by_id(self, db_id):
		db_file = self.alpha.find_one({"_id":ObjectId(db_id)})
		runs = db_file["runs"]
		runs = int(runs)
		runs += 1
		self.alpha.update_one(
	        {"_id": db_id},
			{"$set": {"runs":runs}}
    	)
		return runs

	def db_add_name_to_malware(self, path, name, malware):
		db_file = self.alpha.find_one({'location': path})
		old_name = db_file['Name']

		old_names = []
		if "old_names" in db_file.keys():
			old_names = db_file["old_names"]
		old_names.append(old_name)

		malware.edit_id(db_file['_id'])
		self.db_update_malware_on_id(db_file['_id'], {"old_names":old_names, "Name":name})

	# Used for search
	#uses regular expression to find database items with filename like Chars
	#
	# 	chars - the first charaters of filename looking for
	#TODO extend to use SHA/MD
	def db_find_first_char(self, chars):
		# assert (len) == 1
		# isinstance(s, basestring)

		return self.alpha.find( {'Name': { '$regex': '^' + chars}})

	#NOT USED ANYMORE, USE db_insert_malware_obj
	# def db_insert(self, input_obj):
	# 	assert 'Name' in input_obj
	# 	self.alpha.insert(input_obj)
	#
	# def db_insert_many(self, input_objs):
	# 	for obj in input_objs:
	# 		assert 'Name' in input_obj
	# 		self.alpha.insert(input_obj)


	#inserts a malware object into the database
	#
	# 	malware_obj - a Malware Object
	def db_insert_malware_obj(self, malware_obj):
		db_obj = malware_obj.to_database_file()
		db_id = self.alpha.insert(db_obj)
		malware_obj.edit_id(db_id)
		self.db_gui_insert_newmw()

	#updates a malware sample in the database
	#
	# 	id - the id of the file database object
    # 	update_obj = {
    #     "name":name,
    #     "module":output,
    #     "country":country
	# 	}
	def db_update_malware_on_id(self, id, update_obj):
		self.alpha.update_one(
	        {"_id": id},
			{"$set": update_obj}
    	)

	def db_list_all(self): #Show everything inside the database
		for i in self.alpha.find():
			print (i)

	def db_del_element(self, name,val):	#Remove info from the database
		self.alpha.remove({name:val})

	def db_clear(self):
		self.alpha.delete_many({})
		self.proc.delete_many({})
		self.malware.delete_many({})
		self.average_proctime.delete_many({})



	# THIS IS PROCESS DATABSE STUFF

	#Inserts a process into the database
	#
	#	process - A process object
	def db_proc_insert(self, process):
		db_id = self.proc.insert(process.to_database_file())
		process.edit_id(db_id)

	#Gets all the processes in the database
	def db_get_all_processes(self):
		return self.proc.find()

	#updates a process in the database
	#
	#	process - A process Object
	def db_update_process(self, process_id, update_obj):
		self.proc.update_one(
	        {"_id": process_id},
			{"$set": update_obj}
    	)


Database = Dbio()

#Example usages...
#db_insert_to("0012.mid","25faa9b7d2ff96e3ba424d464580a375","2b110d7bc681eb133f089fd4cdf580ec496c21b9459b474ed33d000f260b4425")
#db_del_element("Name","0012.mid")
#db_list_one("Name","0012.mid")
