#read out or insert in content in database
#Teng++

import pymongo
from pymongo import MongoClient

client = MongoClient('45.32.65.58',27017)
db = client.accenture_t1	#name of the database is "accenture_t1"

#There is a collection called "alpha" in my database, so I need to get it...
alpha = db.alpha
print("\n CONNECT DB SUCCESS! \n")

def db_insert_to(name, md5, sha256):	#Insert a piece of information into the database
	sample = {"Name":name, "MD5":md5, "SHA256":sha256}
	alpha.insert(sample)
	
def db_get_count():	#Get how many items are there in the database
	print('\nThis many--->',alpha.find().count()) 

def db_list_one(name,val): #Show one result using specific rule
	print(alpha.find_one({name:val}))
	
def db_list_all(): #Show everything inside the database
	for i in alpha.find(): 
		print (i)
	
def db_del_element(name,val):	#Remove info from the database
	alpha.remove({name:val})

#Example usages...	
#db_insert_to("0012.mid","25faa9b7d2ff96e3ba424d464580a375","2b110d7bc681eb133f089fd4cdf580ec496c21b9459b474ed33d000f260b4425")
#db_del_element("Name","0012.mid")
#db_list_one("Name","0012.mid")