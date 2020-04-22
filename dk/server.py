from flask import Flask,jsonify,request
import json
import start
import sys
from flask_cors import CORS
import time
import os

lat=None
lon=None
alt=None
app=Flask(__name__)
# from flask_cors import CORS
# from bson.json_util import dumps
from pymongo import MongoClient
import sys
lat=None
lon=None
alt=None

app = Flask(__name__)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
CORS(app)

portno=5750
#COORDINATE API
@app.route('/coordinates', methods=['POST'])
def givelocation():
	try:
		_json = request.json
		src=_json['src']
		des=_json['des']
		src_lat = src['lat']
		src_lon = src['lon']
		des_lat = des['lat']
		des_lon = des['lon']
		global portno
		portno+=10
		start.execute(src_lat,src_lon,des_lat,des_lon,portno)
		time.sleep(5)
		return "SRC Latitude is :"+str(src_lat)+"SRC Longitude is :"+str(src_lon)+"DES Latitude is :"+str(des_lat)+"DEST Longitude is :"+str(des_lon)
	except Exception as e:
		print(e)
	return "Hello World"
@app.route('/beacon', methods=['POST'])
def givebeacon():
	try:
		_json = request.json
		uuid=_json['uuid']
		print "Beacon UUID is :"+str(uuid)
		sys.argv=[uuid]
		#execfile('parser.py')
		#print("Executed Parser")
		execfile('scanner.py')
		print("Started Scanner")
		return "Beacon UUID is :"+str(uuid)
	except Exception as e:
		print(e)
	return "Hello World"
@app.route("/")
def index():
	try:
		f=open("FrcrceData.txt","r")
		l=f.readlines()
		if(len(l)>0):
			st=l[len(l)-1]
			li=st.split(",")
			lat=li[0]
			lon=li[1]
			al=li[2].split("\n")
			alt=al[0]
	except IOError as e:
		lat=None
		lon=None
		alt=None
	return json.dumps({"latitude":lat,"longitude":lon,"alt":alt})

app.run(host='0.0.0.0',port=80,debug=True,threaded=True)

