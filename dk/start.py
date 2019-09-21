import os
import subprocess
import time

# from dronekit_sitl.__init__ import main
def execute(src_lat,src_lon,des_lat,des_lon):
    os.system('fuser -k 5760/tcp')
    os.system('fuser -k 5760/tcp')
# sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
# sys.exit(main())
    f=open("passcoord.txt","w")
    f.write(str(des_lat)+"\n")
    f.write(str(des_lon))
    f.close()
    cmd="dronekit-sitl copter --home="+str(src_lat)+","+str(src_lon)+",0,180&"
    os.system(cmd)

    os.system('screen -dm mavproxy.py --master=tcp:127.0.0.1:5760 --out=127.0.0.1:14550 --out=127.0.0.1:5762')

    os.system('python mission_FRCRCE.py --connect 127.0.0.1:5762')
# subprocess.call("launchSitl")