from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException,Command
import time
import socket
import exceptions
import math
import argparse  #allows us to input values from command line and use it in our function
from pymavlink import mavutil
import datetime
import os
import re
import sys
from pymongo import MongoClient
from bson.json_util import dumps
import sys
import math 


#function#

 

def connectMyCopter():
    #make a parser object
	parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.') 
	parser.add_argument('--connect', help='vehicle connection target string. If not specified, SITL automatically started and used.')  #new argument to specify an IP address after --connect
	args = parser.parse_args()        #this IP address will be captured in args

	connection_string = args.connect   #we'll connect to the IP and save it in a variable
	

	if not connection_string:
		import dronekit_sitl
		sitl= dronekit_sitl.start_default()
		connection_string = sitl.connection_string()


	vehicle = connect(connection_string,wait_ready=True) #input as IP address and dont start script untill we have successfully connected
	vehicle.wait_ready(True,raise_exception=False)
	return vehicle

def arm_and_takeoff(targetHeight):
	while vehicle.is_armable!=True:
		# print("Wait for vehicle to become armable")	
		time.sleep
	print("Vehicle is now armable")

	vehicle.mode = VehicleMode("GUIDED")
	while vehicle.mode!="GUIDED":
		print("Waiting for drone to enter guided mode")	
		time.sleep(1)
	print("Vehicle is now in guided mode")

	vehicle.armed = True
	while vehicle.armed==False:
		print("Waiting for vehicle to become armed")	

		time.sleep(1)

		time.sleep(2)

	print("Propellers are spinning")
	vehicle.simple_takeoff(targetHeight) #meters
	while True:
		print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached")
	return None

#To empty a closed file (whose name is known)

def deleteContent(fName):
    with open(fName, "w"):
        pass
##>> python connection_template.py --connect 127.0.0.1:14550
#Main executable


def printVehicleInformation(vehicle): 
	vehicle.wait_ready('autopilot_version')
	# Get all vehicle attributes (state)
	print("\nGet all vehicle attribute values:")
	print(" Autopilot Firmware version: %s" % vehicle.version)
	print("   Major version number: %s" % vehicle.version.major)
	print("   Minor version number: %s" % vehicle.version.minor)
	print("   Patch version number: %s" % vehicle.version.patch)
	print("   Release type: %s" % vehicle.version.release_type())
	print("   Release version: %s" % vehicle.version.release_version())
	print("   Stable release?: %s" % vehicle.version.is_stable())
	print(" Autopilot capabilities")
	print("   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float)
	print("   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float)
	print("   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int)
	print("   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int)
	print("   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union)
	print("   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp)
	print("   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target)
	print("   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned)
	print("   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int)
	print("   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain)
	print("   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target)
	print("   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination)
	print("   Supports mission_float message type: %s" % vehicle.capabilities.mission_float)
	print("   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
	print(" Global Location: %s" % vehicle.location.global_frame)
	print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
	print(" Local Location: %s" % vehicle.location.local_frame)
	print(" Attitude: %s" % vehicle.attitude)
	print(" Velocity: %s" % vehicle.velocity)
	print(" GPS: %s" % vehicle.gps_0)
	print(" Gimbal status: %s" % vehicle.gimbal)
	print(" Battery: %s" % vehicle.battery)
	print(" EKF OK?: %s" % vehicle.ekf_ok)
	print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
	print(" Rangefinder: %s" % vehicle.rangefinder)
	print(" Rangefinder distance: %s" % vehicle.rangefinder.distance)
	print(" Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
	print(" Heading: %s" % vehicle.heading)
	print(" Is Armable?: %s" % vehicle.is_armable)
	print(" System status: %s" % vehicle.system_status.state)
	print(" Groundspeed: %s" % vehicle.groundspeed)    # settable
	print(" Airspeed: %s" % vehicle.airspeed)    # settable
	print(" Mode: %s" % vehicle.mode.name)    # settable
	print(" Armed: %s" % vehicle.armed)    # settable

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def get_dist_metrs(lat1,lon1,lat2,lon2):
	d_lat = lat1 - lat2
	d_long = lon1 - lon2
	return math.sqrt((d_lat*d_lat) + (d_long*d_long)) * 1.113195e5
def distance_to_current_waypoint():
    """
    Gets distance in metres to the current waypoint. 
    It returns None for the first waypoint (Home location).
    """
    nextwaypoint = vehicle.commands.next
    if nextwaypoint==0:
        return None
    missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint

def current_location():
    return vehicle.location.global_relative_frame

def current_velocity():
	return vehicle.velocity
##>> python connection_template.py --connect 127.0.0.1:14550

#Main executable

#list of commands
if __name__ == "__main__":
	sitl = None
	vehicle = connectMyCopter()
# prints vehicles attributes
	printVehicleInformation(vehicle)

	wphome= vehicle.location.global_relative_frame

	cmd1=None
	cmd2=None
	cmd3=None
	with open("passcoord.txt","r") as f:
		data=f.readlines()
	temp=data[0].split("\n")
	des_lat=float(temp[0])
	des_lon=float(data[1])
	src_lat=wphome.lat
	src_lon=wphome.lon
	deleteContent("passcoord.txt")
	cmd1=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,wphome.lat,wphome.lon,wphome.alt)
	cmd2=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,des_lat,des_lon,15)
	# cmd3=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,19.046592,72.821771,20)
	cmd3=Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,0,0,0,0,0,0,0)



	# Fr Conceicao Rodrigues College of Engineering, Bullock Road, Bandra West, Mumbai - 400050, Maharashtra, India
	#Latitude: 19.044503 | Longitude: 72.820451

	#Hinduja Hospital, Swatantrya Veer Savarkar Marg, G/N Ward, Mumbai - 400016, Maharashtra, India
	#Latitude: 19.033509 | Longitude: 72.838347

 	#Lilavati Hospital, K C Marg, Bandra West, Mumbai - 400050, Maharashtra, India
	#Latitude: 19.051105 | Longitude: 72.829206

	#Mannat, Mon Repos, HK Bhaba Road, H/W Ward, Mumbai - 400050, Maharashtra, India
	#Latitude: 19.04683 | Longitude: 72.82036

	#Mount Mary Ground, Mumbai, Maharashtra, India
		#Latitude: 19.0482 | Longitude: 72.8247

		#Oratory of Our Lady of Fatima, Mount Mary Road, Bandra West, Mumbai - 400050, Maharashtra, India
	#Latitude: 19.046592 | Longitude: 72.821771

	#download current list of commands FROM the drone we are connected to
	cmds= vehicle.commands
	cmds.download()
	cmds.wait_ready()
#dont go further until you have downloaded all the commands from your drone

#download current list of commands FROM the drone we are connected to
	cmds= vehicle.commands
	cmds.download()
	#dont go further until you have downloaded all the commands from your drone
	cmds.wait_ready()



##Clear the current list of commands
	cmds.clear()

##ADD in our new commands
	cmds.add(cmd1)
	cmds.add(cmd2)
	cmds.add(cmd3)
	# cmds.add(cmd4)
	##Upload our commands to the drone
	vehicle.commands.upload()

	arm_and_takeoff(10)
	print("after arm and takeoff") #this is in guided mode
	vehicle.mode=VehicleMode("AUTO")
	while vehicle.mode!="AUTO":
		time.sleep(.2)

	deleteContent("FrcrceData.txt")




	vicinity=False
	while vehicle.location.global_relative_frame.alt>2:
		print("Position: %s"%vehicle.location.global_relative_frame)


		print("Current Realtime location : %s"%current_location())


		#print(type(vehicle.location.global_relative_frame)) 

		#read the actual velocity (m/s)

		print("The actual velocity is %s"%vehicle.velocity) #North,East,Down
		f=open("FrcrceData.txt","a")
		#f.write(str(vehicle.velocity))
		f.write(str(vehicle.location.global_relative_frame.lat)+","+str(vehicle.location.global_relative_frame.lon)+","+str(vehicle.location.global_relative_frame.alt)+"\n")
		lat=vehicle.location.global_relative_frame.lat
		lon=vehicle.location.global_relative_frame.lon
		alt=vehicle.location.global_relative_frame.alt
		#print(type(vehicle.velocity))
			#print("Drone is executing mission, but we can still run code")
		f.close()
		# dt = str(datetime.datetime.now())
		# newname = 'file_'+dt+'.txt'
		# os.rename('FrcrceData.txt', newname)
	#data format
	#Position: LocationGlobalRelative:lat=12.9599052,lon=77.6433314,alt=19.93
	#The actual velocity is [-0.22, 0.01, -0.03]
	#type format list


		clientdist=get_dist_metrs(lat,lon,des_lat,des_lon)
		warehousedist=get_dist_metrs(lat,lon,src_lat,src_lon)

		if(clientdist<=250):
			vicinity=True
		else:
			vicinity=False
		print("Current Realtime velocity is %s"%current_velocity()) #North,East,Down
	
		# creation of MongoClient 
#		client=MongoClient()
		# Connect with the portnumber and host | sudo service mongod start | mongo
		client = MongoClient('mongodb://localhost:27017/') 
		#client = MongoClient('mongodb+srv://drone:drone@cluster0-igbga.mongodb.net/test?retryWrites=true&w=majority') 
#		print('Connect to MongoDB Cluster')
			# Access database 
		mydatabase = client['aidrone'] 
#		print('Created Database')
		# Access collection of the database 
		mycollection=mydatabase['waypoints']
		vel = math.sqrt((vehicle.velocity[0]**2 + vehicle.velocity[1]**2 + vehicle.velocity[2]**2))
		clienttime=clientdist/vel
		warehousetime=warehousedist/vel
		record={ 
		'latitude': vehicle.location.global_relative_frame.lat,
		'longitude': vehicle.location.global_relative_frame.lon,
		'altitude': vehicle.location.global_relative_frame.alt,
		'velocity': {
			'Vx': vehicle.velocity[0],
			'Vy': vehicle.velocity[1],
			'Vz': vehicle.velocity[2]
  			},
		'gimbalStatus': {
			'pitch': vehicle.gimbal.pitch,
			'roll': vehicle.gimbal.roll,
			'pitch': vehicle.gimbal.pitch
		},
		'battery': {
			'voltage': vehicle.battery.voltage,
			'current': vehicle.battery.current,
			'level': vehicle.battery.level
		},
		'lastHeartBeat': vehicle.last_heartbeat,
		'isArmable': vehicle.is_armable,
		'systemStatus': vehicle.system_status.state,
		'groundSpeed': vehicle.groundspeed,
		'airSpeed': vehicle.airspeed,
		'mode': vehicle.mode.name,
		'armed': vehicle.armed,
		'next_waypoint': vehicle.commands.next,
		'distance_to_next_waypoint': distance_to_current_waypoint()
		}
		rec = mydatabase.waypoints.insert(record)
		sys.argv = [vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt, vel, clientdist, warehousedist, vicinity, clienttime, warehousetime ]
		execfile('pushData.py')
		nextwaypoint = vehicle.commands.next
		print('Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint()))
		print("Distance to Client is :",clientdist)
		print("Distance to Warehouse is :",warehousedist)
		print("Time to Client is :",clienttime)
		print("Time to Warehouse is :",warehousetime)
		print("Vicinity status is :",vicinity)
		time.sleep(1)
	
	## Reset variables to sensible values.
	print("\nReset vehicle attributes/parameters and exit")
	vehicle.mode = VehicleMode("STABILIZE")
	#vehicle.armed = False
	vehicle.parameters['THR_MIN']=130
	vehicle.parameters['THR_MID']=500

	print('Return to launch')
	vehicle.mode = VehicleMode("RTL")
	#Close vehicle object before exiting script
	print("\nClose vehicle object")
	vehicle.close()

	# Shut down simulator if it was started.
	if sitl is not None:
	    sitl.stop()

	print("Completed")

