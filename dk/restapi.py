from pymongo import MongoClient
from flask import Flask, jsonify, request 
import json
import requests
import json
import bson
from datetime import datetime
from flask import send_file
import qrcodegen
import pymongo
import re
from flask_restplus import Api, Resource
from flask_swagger import swagger
from flask_cors import CORS
import qrcode
import random
from algo import assignDrones
import start
import ast

client = MongoClient('mongodb+srv://ai-drone:oOIUq8IGcTVKy7JV@cluster0-igbga.mongodb.net/test?retryWrites=true&w=majority',27017)
# client=MongoClient('localhost',27017)
db=client.test
col=db.user
col1=db.drone
col2=db.inventory
col3=db.order
col4=db.mission
col.create_index([('email', pymongo.ASCENDING)], unique=True)
col1.create_index([('name', pymongo.ASCENDING)], unique=True)
col2.create_index([('name', pymongo.ASCENDING)], unique=True)
col4.create_index([('orderid', pymongo.ASCENDING)], unique=True)

# FOR USER APP
db1=client.droneusers
usercol=db1.user


app = Flask(__name__) 
CORS(app)

# STAKEHOLDER APP APIs


@app.route('/signup', methods = ["POST"]) 
def signup():
    print(request)
    print(request.json)
    data=request.json
    print("Data=",data)
    #id=data['id']
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    name=str(data['name'])
    email=str(data['email'])
    password=str(data['password'])
    #Name Validation
    if(len(name)>25):
        return json.dumps(False)
    #Email Validation
    if(re.search(regex,email)==False):
        return json.dumps(False)
    #Password Validation
    flag = 0
    while True:   
        if (len(password)<8): 
            flag = -1
            break
        elif not re.search("[a-z]", password): 
            flag = -1
            break
        elif not re.search("[A-Z]", password): 
            flag = -1
            break
        elif not re.search("[0-9]", password): 
            flag = -1
            break
        elif not re.search("[_@$]", password): 
            flag = -1
            break
        elif re.search("\s", password): 
            flag = -1
            break
        else: 
            flag = 0
            print("Valid Password") 
        break
  
    if flag ==-1: 
        return json.dumps(False)
    for x in col.find():
        print(x)
    print(col.find_one({"email": email}))
    try:
        col.insert({ "name": name, "email":email, "password":password},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)

@app.route('/validateUser', methods = ["POST"]) 
def validateUser():
    data=request.json
    email=str(data['email'])
    password=str(data['password'])
    response = []
    documents=col.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    flag=0
    for i in range(0,len(response)):
        emailreg=response[i]["email"]
        passwordreg=response[i]["password"]
        if(password==passwordreg and email==emailreg):
            flag=1
            break
    if(flag==1):
        return json.dumps(True)
    else:
        return json.dumps(False)

@app.route('/adddrone', methods = ["POST"]) 
def adddrone():
    data=request.json
    name=str(data['name'])
    capacity=data['capacity']
    availability=str(data['availability'])
    image=str(data['image'])
    try:
        col1.insert({ "name": name, "capacity":capacity, "availability":availability,"image":image},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)

@app.route('/getdrones', methods = ["GET"]) 
def getdrones():
    response = []
    documents=col1.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
@app.route('/readDronebyId', methods = ["POST"]) 
def readdronebyid():
    data=request.json
    id=bson.ObjectId(data['_id'])
    response = []
    myquery = { "_id": id }
    documents=col1.find(myquery)
    return json.dumps(documents)

def readdronesbyid(id):
    # data=request.json
    id=bson.ObjectId(id)
    response = []
    myquery = { "_id": id }
    documents=col1.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        # response.append(document)
    return document
@app.route('/updateavailability', methods = ["PUT"]) 
def updateavailability():
    data=request.json
    name=data['name']
    availability=data['availability']
    myquery = { "name": name }
    newvalues = { "$set": { "availability": availability } }
    col1.update_one(myquery, newvalues)
    if(col1.find_one({"name":name})):
        return "Updated"
    else:
        return "No such Drone"
@app.route('/addinventory', methods = ["POST"]) 
def addinventory():
    data=request.json
    #id=data['id']
    name=str(data['name'])
    units=data['units']
    if(units>0):
        availability=True
    else:
        availability=False
    weight=data['weight']
    image=data['image']
    # 
    try:
        col2.insert({ "name": name, "units":units, "availability":availability,"weight":weight,"image":image},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)
@app.route('/readInventoryItembyId', methods = ["POST"]) 
def readinventoryitembyid():
    data=request.json
    id=bson.ObjectId(data['_id'])
    response = []
    myquery = { "_id": id }
    documents=col2.find(myquery)
    return json.dumps(documents)

def readinventoryitemsbyid(id):
    id=bson.ObjectId(id)
    response = []
    myquery = { "_id": id }
    documents=col2.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        # response.append(document)
    return document
@app.route('/fetchinventory', methods = ["GET"]) 
def fetchinventory():
    response = []
    documents=col2.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
@app.route('/updateunits', methods = ["PUT"]) 
def updateunits():
    data=request.json
    name=data['name']
    units=data['units']
    myquery = { "name": name }
    newvalues = { "$set": { "units": units } }
    col2.update_one(myquery, newvalues)
    if(units==0):
        myquery = { "name": name }
        newvalues = { "$set": { "availability": False } }
        col2.update_one(myquery, newvalues)
    else:
        myquery = { "name": name }
        newvalues = { "$set": { "availability": True } }
        col2.update_one(myquery, newvalues)
    if(col2.find_one({"name":name})):
        return "Updated units"
    else:
        return "No such item found"
@app.route('/addorder', methods = ["POST"]) 
def addorder():
    data=request.json
    assigneddrones=data['AssignedDrones']
    dateTimeObj = datetime.now()
    timestamp=dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    timestamp=timestamp[:-5]
    timestamp+=")"
    odid=col3.insert({ "AssignedDrones": assigneddrones, "timestamp":timestamp},check_keys=False)
    ans={}
    ans['orderId']=str(odid)
    return json.dumps(ans)
    # return json.dumps(True)
@app.route('/readOrdersById', methods = ["POST"]) 
def readordersbyid():
    data=request.json
    id=bson.ObjectId(data['_id'])
    response = []
    myquery = { "_id": id }
    documents=col3.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        document['AssignedDrones']=(document['AssignedDrones'])
        print(document)
        print(document['_id'])
        print(document['AssignedDrones'])

        for x in document['AssignedDrones']:
            droneId = x['droneid']
            x['drone'] = readdronesbyid(droneId)
            del x['droneid']
            for y in x['inventoryItems']:
                inventoryId = y['inventoryid']
                y['inventory'] = readinventoryitemsbyid(inventoryId)
                del y['inventoryid']
                qty=y['quantity']
                y['inventory']['quantity']=qty
                y['inventoryitem']=y['inventory']
                del y['inventory']    
        response.append(document)
        print("Response is")
        print(response) 
    print(response)
    return json.dumps(document)    

def readallordersbyid(id):
    print("Hello i am here")
    id=bson.ObjectId(id)
    response = []
    myquery = { "_id": id }
    documents=col3.find(myquery)
    for document in documents:
        print("DOCUMENT")
        print(document)
        document['_id'] = str(document['_id'])
        document['AssignedDrones']=(document['AssignedDrones'])

        print("In here")
        print("Assigned Drones are :",document['AssignedDrones'])
        for x in document['AssignedDrones']:
            print("A")
            droneId = x['droneid']
            print("B")
            x['drone'] = readdronesbyid(droneId)
            print("C")
            del x['droneid']
            print("D")
            for y in x['inventoryItems']:
                inventoryId = y['inventoryid']
                y['inventory'] = readinventoryitemsbyid(inventoryId)
                del y['inventoryid']
                qty=y['quantity']
                y['inventory']['quantity']=qty
                y['inventoryitem']=y['inventory']
                del y['inventory']
                del y['quantity']
                # print(inventoryId)   
            print("E")
        print("Out here")
            # newlist.append(x[0])
        # print(type(document['AssignedDrones']))
        # document['AssignedDrones']=newlist
        response.append(document)
        # print("Response is")
        # print(response)
    print("Hello From Orders")
    # print("Document is :",document)
    print("Response is :",response)
    return json.dumps(response)


@app.route('/fetchorders', methods = ["GET"]) 
def fetchorders():
    response = []
    documents=col3.find()
    for document in documents:
        for x in document['AssignedDrones']:
            droneId = x['droneid']
            x['drone'] = readdronesbyid(droneId)
            for y in x['inventoryItems']:
                inventoryId = y['inventoryid']
                y['inventory'] = readinventoryitemsbyid(inventoryId)
                print(inventoryId)
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
@app.route('/createmission', methods = ["POST"]) 
def createmission():
    data=request.json
    #id=data['id']
    orderid=data['orderId']
    # dateOfMission=data["dateOfMission"]
    # timeOfDeparture=data["timeOfDeparture"]
    # timeOfDelivery=data["timeOfDelivery"]
    # timeOfArrival=data["timeOfArrival"]
    # distanceTravelled=data["distanceTravelled"]
    From=data["from"]
    To=data["to"]
    src_lat=data['src_lat']
    src_lon=data['src_lon']
    dest_lat=data['dest_lat']
    dest_lon=data['dest_lon']
    # clientPhotograph=data["clientPhotograph"]
    # waypoints=data["waypoints"]
    params = {
	"src":{
		"lat":src_lat,
		"lon":src_lon
	},
	"des":{
		"lat":dest_lat,
		"lon":dest_lon
	}
}
    headers = {'content-type': 'application/json'}
    response = requests.post(
    'http://13.234.119.101/generate-waypoints',
    data=json.dumps(params),headers=headers)
    wp=response.json()
    print("WP :",wp)
    waypoints=[]
    for i in range(0,len(wp)):
        waypoints.append(wp[i]["waypoint"])
    print("Waypoints are :",waypoints)
    try:
        # col4.insert({"orderid": orderid, "dateOfMission":dateOfMission,
        # "timeOfDeparture":timeOfDeparture,"timeOfDelivery":timeOfDelivery,"timeOfArrival":timeOfArrival,
        # "distanceTravelled":distanceTravelled,"From":From,"To":To,
        # "clientPhotograph":clientPhotograph,"waypoints":waypoints},check_keys=False)
        mid=col4.insert({"orderid": orderid,"from":From,"to":To,"waypoints":waypoints},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    ans={}
    ans['mission_id']=str(mid)
    print("Answer is :",ans)
    print(type(ans))
    return json.dumps(ans)
@app.route('/readmissions', methods = ["GET"]) 
def readmissions():
    # id=bson.ObjectId(data['_id'])
    print("Read Missions")
    response = []
    # myquery = { "_id": id }
    documents=col4.find()
    for document in documents:
        orderid=bson.ObjectId(document['orderid'])
        print("Hello")
        document['order']=readallordersbyid(orderid)
        print("World")
        del document['orderid']
        document['_id'] = str(document['_id'])
        response.append(document)
    print("Response",response)
    return json.dumps(response)
@app.route('/readMissionById', methods = ["POST"]) 
def readmissionbyid():
    data=request.json
    id=bson.ObjectId(data['_id'])
    response = []
    myquery = { "_id": id }
    documents=col4.find(myquery)
    for document in documents:
        orderid=bson.ObjectId(document['orderid'])
        document['order']=readallordersbyid(orderid)
        del document['orderid']
        document['_id'] = str(document['_id'])
        response.append(document)
    print("Response",response)
    return json.dumps(response)
    # return json.dumps(document) 
@app.route('/deleteMissionById', methods = ["DELETE"]) 
def deletemissionbyid():
    data=request.json
    id=data['_id']
    response = []
    myquery = { "_id": id }
    x = col4.delete_many(myquery)
    if(x.deleted_count>0):
        return True
    else:
        return False
@app.route('/get_image')
def get_image():
    qrcodegen.genqrcode()
    if request.args.get('type') == '1':
       filename = 'code.jpg'
    else:
       filename = 'code.jpg'
    return send_file(filename, mimetype='image/gif')


@app.route('/assigndrone', methods = ["POST"]) 
def assigndrone():
    response = []
    dronesavailable=[]
    documents=col1.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    data=request.json
    print("Response is :",response)
    for item in response:
        print("Item is :",item)
        if(item['availability']=='True'):
            dronesavailable.append([item['_id'],item['name'],item['capacity'],item['availability'],item['image']])
    print("Available drones are :")
    print(dronesavailable)
    id=[product['_id'] for product in data['product']]
    weight=[product['weight'] for product in data['product']]
    units=[product['units'] for product in data['product']]
    name=[product['name'] for product in data['product']]
    availability=[product['availability'] for product in data['product']]
    image=[product['image'] for product in data['product']]

    for i in range(0,len(units)):
        if(units[i]>1):
            for j in range(1,units[i]):
                id.insert(i+1,id[i])
                weight.insert(i+1,weight[i])
                name.insert(i+1,name[i])
                availability.insert(i+1,availability[i])
                image.insert(i+1,image[i])
                units[i]=1
                units.insert(i+1,1)
    for i in range(0,len(dronesavailable)-1):
        for j in range(i+1,len(dronesavailable)):
            if(dronesavailable[i][2]>dronesavailable[j][2]):
                dronesavailable[i],dronesavailable[j]=dronesavailable[j],dronesavailable[i]
    print("Drones after arranging in decreasing order of their weight carrying capacity",dronesavailable)
    print("Id's are :",id)
    print("Weights are :",weight)
    visited=[]
    for i in range(0,len(weight)):
        visited.append(0)
    dronespace=[]
    dronesinfo=[]
    for i in range(0,len(dronesavailable)):
        dronespace.append(dronesavailable[i][2])
    for i in range(0,len(dronesavailable)):
        dronesinfo.append(dronesavailable[i])
    for i in range(0,len(dronesinfo)-1):
        for j in range(i+1,len(dronesinfo)):
            if(dronesinfo[i][2]<dronesinfo[j][2]):
                dronesinfo[i],dronesinfo[j]=dronesinfo[j],dronesinfo[i]
    for i in range(0,len(dronespace)-1):
        for j in range(i+1,len(dronespace)):
            if(dronespace[i]<dronespace[j]):
                dronespace[i],dronespace[j]=dronespace[j],dronespace[i]
    print("Drone Space is : ",dronespace)
    assigneddronesvalue=assignDrones(dronespace,weight)
    print("Assigned Drones are :",assigneddronesvalue)
    finalans=[]
    for i in range(0,len(assigneddronesvalue)):
        if(assigneddronesvalue[i]!=0):
            val=[]
            droneval={}
            inventoryval={}
            for j in range(0,len(assigneddronesvalue[i])):
                ind=weight.index(assigneddronesvalue[i][j])
                inventoryval['inventory_id']=id[ind]
                inventoryval['inventory_name']=name[ind]
                inventoryval['inventory_weight']=weight[ind]
                inventoryval['quantity']=1
                inventoryval['inventory_image']=image[ind]
                # val.append([id[ind],weight[ind]])
                val.append(inventoryval)
                weight[ind]=-1
                key=str(dronesinfo[i])
            for j in range(0,len(val)-1):
                if(val[j]!=0):
                    for k in range(j+1,len(val)):
                        if(val[j]['inventory_id']==val[k]['inventory_id']):
                            val[j]['quantity']+=1
                            val[k]=0
            val=list(filter(lambda a: a != 0, val))
            droneval['drone_id']=dronesinfo[i][0]
            droneval['drone_name']=dronesinfo[i][1]
            droneval['drone_capacity']=dronesinfo[i][2]
            droneval['drone_availability']=dronesinfo[i][3]
            droneval['drone_image']=dronesinfo[i][4]
            droneval['inventoryItems']=val
            finalans.append(droneval)
                # finalans[key]=val
    print("Final Answer is :",finalans)
    return json.dumps(finalans)

#USER APP APIS START HERE

qrcodenumber=-1
qrscannumber=-1


@app.route('/usersignup', methods = ["POST"]) 
def usersignup():
    print(request)
    print(request.data)
    data=request.data
    data = json.loads(data.decode('utf8'))
    print("Data=",data)
    #id=data['id']
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    name=str(data['name'])
    email=str(data['email'])
    password=str(data['password'])
    #Name Validation
    if(len(name)>25):
        return json.dumps(False)
    #Email Validation
    if(re.search(regex,email)==False):
        return json.dumps(False)
    #Password Validation
    flag = 0
    while True:   
        if (len(password)<8): 
            flag = -1
            break
        elif not re.search("[a-z]", password): 
            flag = -1
            break
        elif not re.search("[A-Z]", password): 
            flag = -1
            break
        elif not re.search("[0-9]", password): 
            flag = -1
            break
        elif not re.search("[_@$]", password): 
            flag = -1
            break
        elif re.search("\s", password): 
            flag = -1
            break
        else: 
            flag = 0
            print("Valid Password") 
        break
  
    if flag ==-1: 
        return json.dumps(False)
    for x in usercol.find():
        print(x)
    print(usercol.find_one({"email": email}))
    try:
        usercol.insert({ "name": name, "email":email, "password":password},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)

@app.route('/userValidation', methods = ["POST"]) 
def UserValidation():
    data=request.data
    data = json.loads(data.decode('utf8'))
    print(data)
    email=str(data['email'])
    password=str(data['password'])
    print(email)
    print(password)
    response = []
    documents=usercol.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    flag=0
    for i in range(0,len(response)):
        emailreg=response[i]["email"]
        passwordreg=response[i]["password"]
        if(password==passwordreg and email==emailreg):
            flag=1
            break
    if(flag==1):
        return json.dumps(True)
    else:
        return json.dumps(False)   


@app.route('/getQrCode', methods = ["POST"]) 
def getQrCode():
    data=request.data
    data = json.loads(data.decode('utf8'))
    number=random.randint(1,100)
    number=number*random.randint(1,100)
    number=number*random.randint(1,100)
    number=number*random.randint(1,100)
    number=number*random.randint(1,100)
    print(number)
    global qrcodenumber
    qrcodenumber=number    
    return json.dumps(number)

@app.route('/setQrScanNumber', methods = ["POST"]) 
def setQrScanNumber():
    data=request.form['qrscannumber']
    print("Data is :",data)
    global qrscannumber
    qrscannumber=data
    print(qrscannumber)
    return json.dumps(True)

@app.route('/checkQrCode', methods = ["POST"]) 
def checkQrCode():
    data=request.data
    data = json.loads(data.decode('utf8'))
    print(data)
    global qrcodenumber
    global qrscannumber
    print("Hello")
    print("QRCODE SCAN NUMBER  :",qrscannumber)
    print("QRCODE GEN NUMBER :",qrcodenumber)
    if(str(qrcodenumber)==str(qrscannumber)):
        qrscannumber=-1
        return json.dumps(True)
    else:
        return json.dumps(False)



# DRONE BASED APIS

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

if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=80,debug = True)

        
   
