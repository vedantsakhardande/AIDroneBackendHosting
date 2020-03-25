from pymongo import MongoClient
from flask import Flask, jsonify, request 
import json
from datetime import datetime
from flask import send_file
import qrcodegen
import pymongo



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


app = Flask(__name__) 
  
# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/signup', methods = ["POST"]) 
def signup():
    data=request.json
    #id=data['id']
    name=str(data['name'])
    email=str(data['email'])
    password=str(data['password'])
    for x in col.find():
        print(x)
    print(col.find_one({"email": email}))
    # if(col.find_one({"email": email})):
    #     print(col.find_one({"email": email}))
    #     return "Already Registered"
    # else:
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
    # print(type(response[0]))
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
    #id=data['id']
    name=str(data['name'])
    capacity=data['capacity']
    availability=str(data['availability'])
    image=str(data['image'])
    # if(col1.find_one({"name": name})):
    #     print(col1.find_one({"name": name}))
    #     return "Drone already registered"
    # else:
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
    id=data['_id']
    response = []
    myquery = { "_id": id }
    documents=col1.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
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
    id=data['_id']
    response = []
    myquery = { "_id": id }
    documents=col2.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
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
    #id=data['id']
    assigneddrones=data['AssignedDrones']
    dateTimeObj = datetime.now()
    timestamp=dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    timestamp=timestamp[:-5]
    timestamp+=")"
    # if(col3.find_one({"id": id})):
    #     print(col3.find_one({"id": id}))
    #     return "Order with same ID is present"
    # else:
    col3.insert({ "AssignedDrones": assigneddrones, "timestamp":timestamp},check_keys=False)
    return json.dumps(True)
@app.route('/readOrdersById', methods = ["POST"]) 
def readordersbyid():
    data=request.json
    id=data['_id']
    response = []
    myquery = { "_id": id }
    documents=col3.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)    
@app.route('/fetchorders', methods = ["GET"]) 
def fetchorders():
    response = []
    documents=col3.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
@app.route('/createmission', methods = ["POST"]) 
def createmission():
    data=request.json
    #id=data['id']
    orderid=data['orderId']
    dateOfMission=data["dateOfMission"]
    timeOfDeparture=data["timeOfDeparture"]
    timeOfDelivery=data["timeOfDelivery"]
    timeOfArrival=data["timeOfArrival"]
    distanceTravelled=data["distanceTravelled"]
    From=data["from"]
    To=data["to"]
    clientPhotograph=data["clientPhotograph"]
    waypoints=data["waypoints"]
    # if(col4.find_one({"orderid": orderid})):
    #     print(col4.find_one({"orderid": orderid}))
    #     return "Mission already registered"
    # else:
    try:
        col4.insert({"orderid": orderid, "dateOfMission":dateOfMission,
        "timeOfDeparture":timeOfDeparture,"timeOfDelivery":timeOfDelivery,"timeOfArrival":timeOfArrival,
        "distanceTravelled":distanceTravelled,"From":From,"To":To,
        "clientPhotograph":clientPhotograph,"waypoints":waypoints},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return False
    return True
@app.route('/readmissions', methods = ["GET"]) 
def readmissions():
    response = []
    documents=col4.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)
@app.route('/readMissionById', methods = ["POST"]) 
def readmissionbyid():
    data=request.json
    id=data['_id']
    response = []
    myquery = { "_id": id }
    documents=col4.find(myquery)
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)  
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
    for item in response:
        if(item['availability']=='True'):
            dronesavailable.append([item['id'],item['name'],item['capacity']])
    print("Available drones are :")
    print(dronesavailable)
    id=[product['id'] for product in data['product']]
    weight=[product['weight'] for product in data['product']]
    units=[product['units'] for product in data['product']]
    name=[product['name'] for product in data['product']]
    availability=[product['availability'] for product in data['product']]
    # image=[product['image'] for product in data['product']]

    for i in range(0,len(units)):
        if(units[i]>1):
            for j in range(1,units[i]):
                id.insert(i+1,id[i])
                weight.insert(i+1,weight[i])
                name.insert(i+1,name[i])
                availability.insert(i+1,availability[i])
                units[i]=1
                units.insert(i+1,1)
    


    for i in range(0,len(dronesavailable)-1):
        for j in range(i+1,len(dronesavailable)):
            if(dronesavailable[i][2]>dronesavailable[j][2]):
                dronesavailable[i],dronesavailable[j]=dronesavailable[j],dronesavailable[i]
    print("Drones after arranging in decreasing order of their weight carrying capacity",dronesavailable)

    print("ID's are :",id)
    print("Weight's are :",weight)
    print("QTY are :",units)
    print("Availabilty are :",availability)
    print("Name are :",name)
    sumofweights=0
    dronesreqd=[]
    for i in range(0,len(weight)):
        sumofweights+=weight[i]
    visited=[]
    for i in range(0,len(dronesavailable)):
        visited.append(0)
    i=0
    print("Sum of weights :",sumofweights)
    while(sumofweights>0):
        flag=0     
        while(dronesavailable[i][2]<sumofweights and i<len(dronesavailable)):
            i+=1
            flag=1
            if(i==len(dronesavailable)):
                break

        if(i==len(dronesavailable) and visited[i-1]==1):
            print("No drone available")
        elif(flag==1):
            if(visited[i-1]==1):
                continue
            else:
                print("HHHHHHEEEEEEELLLLLLOOOOOOOO",i-1)
                dronesreqd.append(dronesavailable[i-1])
                sumofweights=sumofweights-dronesavailable[i-1][2]
                visited[i-1]=1
        else:
            for k in range(0,len(visited)):
                if(visited[k]==0):
                    break
            print("HHHHHHEEEEEEELLLLLLOOOOOOOO",k)
            dronesreqd.append(dronesavailable[k])
            sumofweights=sumofweights-dronesavailable[k][2]
            visited[k]=1
        print(sumofweights)
        i=0
    print(dronesreqd)
    #CHECK FROM HERE
    for i in range(0,len(weight)-1):
        for j in range(i+1,len(weight)):
            if(weight[i]<weight[j]):
                weight[i],weight[j]=weight[j],weight[i]
                id[i],id[j]=id[j],id[i]
                units[i],units[j]=units[j],units[i]
                name[i],name[j]=name[j],name[i]
                availability[i],availability[j]=availability[j],availability[i]
    i=0
    j=0
    weightleft=dronesreqd[i][2]
    assigneddrones=[]
    while(weight[j]<=weightleft):
        assigneddrones.append([id[j],name[j],availability[j],units[j],weight[j]])
        weightleft=dronesreqd[i][2]-weight[j]
        j+=1
        if(j==len(weight)):
            break
        else:
            if(weight[j]>weightleft):
                i+=1
                weightleft=dronesreqd[i][2]
    print("Assigned Drones are :",assigneddrones)
    finalresponse=[]
    for i in range(0,len(dronesreqd)):
        finalresponse.append(
            {
                "id":dronesreqd[i][0],
                "name":dronesreqd[i][1],
                "capacity":dronesreqd[i][2],
                "inventoryItems":assigneddrones[i]
            }
            )

    return json.dumps(finalresponse)
            


if __name__ == '__main__': 
  
    app.run(debug = True) 