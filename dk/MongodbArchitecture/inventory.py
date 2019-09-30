import datetime
 
# from database import DB
from flask import jsonify
import pymongo
import json
from bson import json_util
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sampleapp"]
mycol = mydb["inventory"]
class Drone(object):
    @staticmethod
    def insert_one(data):
	x = mycol.insert_one(mydict)
	print(x.inserted_id)   
    @staticmethod
    def insert_many(data): 
	x = mycol.insert_one(data)
	print(x.inserted_ids)  
    @staticmethod 
    def find_one(query): #make it work for thus one

        result=[]
        for x in mycol.find_one({},query):
            result.append({'_id' : x['_id'],'title' : x['title']})
            print(x['_id']) # Object ID
            # print(x)
        return result
    @staticmethod 
    def find_many(query): #make it work for thus one
        result=[]
        for x in mycol.find({},query):
            result.append({'_id' : x['_id'],'title' : x['title']})
            print(x['_id']) # Object ID
            # print(x)
        return result
    @staticmethod
    def replace_one(title,data):
	result = mycol.replace_one({"title":title}, data)
	print("Data replaced with title",result)
	return result
    @staticmethod
    def replace_many(title,data):
	result = mycol.replace_many({"title":title}, data)
	print("Data replaced with title",result)
	return result
    @staticmethod 
    def update_one(src,dest):
	x =mycol.update_one(src, dest)
	print(x.modified_count, "documents updated.") 
	return str(x.modified_count)+" documents updated"
    @staticmethod 
    def update_many(src,dest):
	x =mycol.update_many(src, dest)
	print(x.modified_count, "documents updated.") 
	return str(x.modified_count)+" documents updated"
    @staticmethod 
    def delete_one(query):
	x=mycol.delete_one(query)
	print(x.deleted_count, " documents deleted.") 
	return str(x.deleted_count)+" documents deleted"
    @staticmethod 
    def delete_many(query):
	x=mycol.delete_many(query)
	print(x.deleted_count, " documents deleted.") 
	return str(x.deleted_count)+" documents deleted"



#make it work for thus one	
    # @staticmethod
    # def find_one(query):
    #     return DB.find(collection='drones')
    #Why two? sorry

    @staticmethod
    def deleteOne(query): # and this one
        return DB.deleteOne(collection='inventory',query={'title':'Mavic Air'})


 
