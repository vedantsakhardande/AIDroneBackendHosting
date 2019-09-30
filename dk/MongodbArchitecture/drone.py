import datetime
 
# from database import DB
from flask import jsonify
import pymongo
import json
from bson import json_util
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sampleapp"]
mycol = mydb["drones"]
class Drone(object):
    @staticmethod
    def insert(data):
        DB.insert(collection='drones', data=data)
    
    @staticmethod 
    def find_one(query): #make it work for thus one

        result=[]
        for x in mycol.find({},query):
            result.append({'_id' : x['_id'],'title' : x['title']})
            print(x['_id']) # Object ID
            # print(x)
        return result
    
    # @staticmethod
    # def find_one(query):
    #     return DB.find(collection='drones')
    #Why two? sorry

    @staticmethod
    def deleteOne(query): # and this one
        return DB.deleteOne(collection='drones',query={'title':'Mavic Air'})
 