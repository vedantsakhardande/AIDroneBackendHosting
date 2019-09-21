from pymongo import MongoClient 
  

try: 
    print("Hi")
    # client = MongoClient("mongodb+srv://dronedata:dronedata@cluster0-iuvph.mongodb.net/test?retryWrites=true&w=majority")
    client=MongoClient()
    print("Hello")
    db = client['dronedata']
    print("Connected successfully!!!") 
  
# Created or Switched to collection names: my_gfg_collection 
    collection = db.dronedata
    l=[10,12,13]
    l1=l[0]
    l2=l[1]
    l3=l[2]
    emp_rec1 = { 
        "latitude":str(l1),
        "longitude":str(l2),
        "altitude":str(l3)
        } 
# Insert Data 
    rec_id1 = collection.insert_one(emp_rec1) 
  
    print("Data inserted with record ids",rec_id1) 
    cursor = collection.find() 
    for record in cursor: 
        print(record) 

except:   
    print("Could not connect to MongoDB") 
  
# database 
  
# Printing the data inserted 
