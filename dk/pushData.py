import pusher
import sys
import json
channels_client = pusher.Pusher(
  app_id='854249',
  key='980f167a4cd9ef7b753c',
  secret='20100273d7a6e08aa578',
  cluster='ap2',
  ssl=True
)
with open("beaconstatus.txt","r") as f:
  data=f.readlines()
f.close()
beaconstatus=data[0]
channels_client.trigger('my-channel', 'my-event',
                        json.dumps({'latitude': round(sys.argv[0],5),
                         'longitude': round(sys.argv[1],5),
                         'altitude': round(sys.argv[2],5),
                         'velocity': round(sys.argv[3],5),
                         'clientdist': round(sys.argv[4],5),
                         'warehousedist': round(sys.argv[5],5),
                         'vicinity': round(sys.argv[6],5),
                         'clienttime': round(sys.argv[7],5),
                         'warehousetime': round(sys.argv[8],5),
                         'beaconstatus': beaconstatus})),
                          