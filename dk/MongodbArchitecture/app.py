# so app.py calls methods from drones.py (which is a object like java) and that calls methods
# from database.py [Which is generic for any object] 
# Let me give an example


from flask import Flask, jsonify,request
import json
# from database import DB
# from job import Job
from drone import Drone
from flask_cors import CORS
from bson import json_util
app = Flask(__name__)
CORS(app)
# DB.init()

@app.route('/insert-drone', methods=['POST'])
def insertDrone():
    data = {
        'title':'Mavic Air',
        'capacity':5,
        'status':'Available',
        'health': 'healthy',
        'model': '125 MUX',
        'motorCount': 4,
        'batteryType': 'Lipo'
    }
    Drone.insert(data)  
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
def deleteDrone():
    data = {
        'title':'Mavic Air',
        'capacity':5,
        'status':'Available',
        'health': 'healthy',
        'model': '125 MUX',
        'motorCount': 4,
        'batteryType': 'Lipo'
    }
    return 'successfully inserted drone'
@app.route('/delete-drone', methods=['DELETE'])
def deleteDrone():
    Drone.deleteOne(query={'title':'Mavic Air'}) 
app.run(host='127.0.0.1',port=5000,debug=True)