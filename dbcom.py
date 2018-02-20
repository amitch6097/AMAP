import pymongo
from pymongo import MongoClient

client = MongoClient('45.32.65.58',27017)
db = client.accenture_t1	#name of the database is "accenture_t1"

#There is a collection called "alpha" in my database, so I need to get it...
alpha = db.alpha
print("\n CONNECT DB SUCCESS! \n")

#Now insert new info
sample = {"Name":"CIH", "MD5":"1A2B3C4D", "SHA256":"1234"}
alpha.insert(sample)
#####################
print('\nThis many--->',alpha.find().count()) #How many now?

for i in alpha.find(): #Now listing everything
	print (i)
	
	
alpha.remove({"MD5":"111"})   #Remove one