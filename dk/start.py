import os
import subprocess
import time

# from dronekit_sitl.__init__ import main
def execute(src_lat,src_lon,des_lat,des_lon,portno):
    #os.system('fuser -k 5760/tcp')
    #os.system('fuser -k 5760/tcp')
    killport='fuser -k '+str(portno)+'/tcp'
    print("Killport",killport)
    os.system(killport)
    os.system(killport)
# sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
# sys.exit(main())
    f=open("passcoord.txt","w")
    f.write(str(des_lat)+"\n")
    f.write(str(des_lon))
    f.close()
    if(portno==5760):
    	cmd="dronekit-sitl copter --home="+str(src_lat)+","+str(src_lon)+",0,180&"
    else:
	instanceno=(portno-5760)//10
	cmd="dronekit-sitl copter --instance "+str(instanceno)+" --home="+str(src_lat)+","+str(src_lon)+",0,180&"
    os.system(cmd)
    time.sleep(2)
    screenstr="screen -dm mavproxy.py --master=tcp:127.0.0.1:"+str(portno)+" --out=127.0.0.1:14550 --out=127.0.0.1:"+str(portno+5)
    print str(screenstr)
    os.system(screenstr)
    #os.system('screen -dm mavproxy.py --master=tcp:127.0.0.1:5760 --out=127.0.0.1:14550 --out=127.0.0.1:5762')
    time.sleep(2)
    missionstr="python mission_FRCRCE.py --connect 127.0.0.1:"+str(portno+5)
    #os.system('python mission_FRCRCE.py --connect 127.0.0.1:5762')
    print str(missionstr)
    os.system(missionstr)
# subprocess.call("launchSitl")
