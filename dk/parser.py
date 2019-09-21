from beacontools import parse_packet

if __name__ == "__main__":
    while(True):
        ibeacon_packet = b"\x02\x01\x06\x1a\xff\x4c\x00\x02\x15\x41\x41\x41\x41\x41\x41\x41\x41\x41" \
                        b"\x41\x41\x41\x41\x41\x41\x41\x00\x01\x00\x01\xf8"
        adv = parse_packet(ibeacon_packet)
        print("UUID: %s" % adv.uuid)
        print("Major: %d" % adv.major)
        print("Minor: %d" % adv.minor)
        print("TX Power: %d" % adv.tx_power)
        f=open("beaconstatus.txt","w")
        if(adv):
            f.write("Successful")
            break
        else:
            f.write("Unsuccessful")
        f.close()