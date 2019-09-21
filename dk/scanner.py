import time
from beacontools import BeaconScanner, IBeaconFilter

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

# scan for all iBeacon advertisements from beacons with the specified uuid
if __name__ == "__main__":
    scanner = BeaconScanner(callback,
        device_filter=IBeaconFilter(uuid=str(sys.argv[0]))
    )
    print("Scanner returned : ",scanner.start())
    time.sleep(5)
    scanner.stop()

