#read out or insert in content in database
#Teng++

import pymongo
from pymongo import MongoClient

class Dbio:
	def __init__(self):
		client = MongoClient('45.32.65.58',27017)
		db = client.accenture_t1	#name of the database is "accenture_t1"

		#There is a collection called "alpha" in my database, so I need to get it...
		self.alpha = db.alpha
		print("\n CONNECT DB SUCCESS! \n")

	def db_insert_to(self, name, md5, sha256):	#Insert a piece of information into the database
		sample = {"Name":name, "MD5":md5, "SHA256":sha256}
		self.alpha.insert(sample)

	def db_get_count(self):	#Get how many items are there in the database
		return '\nThis many--->',self.alpha.find().count()

	def db_list_one(self, name,val): #Show one result using specific rule
		return self.alpha.find_one({name:val})

	def db_find_first_char(self, chars):
		# assert (len) == 1
		# isinstance(s, basestring)

		return self.alpha.find( {'Name': { '$regex': '^' + chars}})


	def db_list_all(self): #Show everything inside the database
		for i in self.alpha.find():
			print (i)

	def db_del_element(self, name,val):	#Remove info from the database
		self.alpha.remove({name:val})

#Example usages...
#db_insert_to("0012.mid","25faa9b7d2ff96e3ba424d464580a375","2b110d7bc681eb133f089fd4cdf580ec496c21b9459b474ed33d000f260b4425")
#db_del_element("Name","0012.mid")
#db_list_one("Name","0012.mid")
