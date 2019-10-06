# so app.py calls methods from drones.py (which is a object like java) and that calls methods
# from database.py [Which is generic for any object] 
# Let me give an example


from flask import Flask, jsonify,request
import json
# from database import DB
# from job import Job
from drone import Drone
from inventory import Inventory
from flask_cors import CORS
from bson import json_util
app = Flask(__name__)
CORS(app)
# DB.init()

@app.route('/insert-drone', methods=['POST'])
def insertDrone():
    
    try:
        _json = request.json
        title=_json['title']
        capacity=_json['capacity']
        status=_json['status']
        health=_json['health']
        model=_json['model']
        motorCount=_json['motorCount']
        batteryType=_json['batteryType']
        data = {
        'title':title,
        'capacity':capacity,
        'status':status,
        'health': health,
        'model': model,
        'motorCount': motorCount,
        'batteryType': batteryType
    }
    except Exception as e:
        print(e)
    Drone.insert_one(data)  
    return 'successfully inserted drone'
@app.route('/find-drone', methods=['GET'])
def findDrone():
    #recieve that here first and give to query
    try:
        _json = request.json
        title=_json['title']
    except Exception as e:
        print(e)
    query = {'title': title}
    return json_util.dumps(Drone.find_one(query))
@app.route('/find-drones', methods=['GET'])
def findDrones():
    #recieve that here first and give to query
    try:
        _json = request.json
        title=_json['title']
    except Exception as e:
        print(e)
    query = {'title': title}
    return json_util.dumps(Drone.find_many(query))
@app.route('/delete-drone', methods=['DELETE'])
def deleteDrone():
    try:
        _json = request.json
        title=_json['title']
        return Drone.delete_one(query={'title':'Mavic Air'})
    except Exception as e:
        print(e)
    return "Nothing Deleted" 


#INVENTORY
@app.route('/insert-item', methods=['POST'])
def insertItem():
    
    try:
        _json = request.json
        title=_json['title']
        weight=_json['weight']
        price=_json['price']
        data = {
        'title':title,
        'weight':weight,
        'price':price
    }
    except Exception as e:
        print(e)
    Inventory.insert_one(data)  
    return 'successfully inserted drone'
@app.route('/find-item', methods=['GET'])
def findItem():
    #recieve that here first and give to query
    try:
        _json = request.json
        title=_json['title']
    except Exception as e:
        print(e)
    query = {'title': title}
    return json_util.dumps(Inventory.find_one(query))
@app.route('/find-items', methods=['GET'])
def findItems():
    #recieve that here first and give to query
    try:
        _json = request.json
        title=_json['title']
    except Exception as e:
        print(e)
    query = {'title': title}
    return json_util.dumps(Inventory.find_many(query))
@app.route('/delete-item', methods=['DELETE'])
def deleteItem():
    try:
        _json = request.json
        title=_json['title']
        return Inventory.delete_one(query={'title':'CS GO'})
    except Exception as e:
        print(e)
    return "Nothing Deleted" 
app.run(host='127.0.0.1',port=5000,debug=True)
