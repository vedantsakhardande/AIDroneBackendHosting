from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import json
import requests

# get the webcam:  


def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects

val=""

def getandcheckqr():
  print("Here")
  cap = cv2.VideoCapture(0)

  cap.set(3,640)
  cap.set(4,480)
  #160.0 x 120.0
  #176.0 x 144.0
  #320.0 x 240.0
  #352.0 x 288.0
  #640.0 x 480.0
  #1024.0 x 768.0
  #1280.0 x 1024.0
  time.sleep(2)
  font = cv2.FONT_HERSHEY_SIMPLEX

  while(cap.isOpened()):
    # Capture frame-by-frame
      ret, frame = cap.read()
    # Our operations on the frame come here
      im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
      decodedObjects = decode(im)
      flag=0
      for decodedObject in decodedObjects: 
          points = decodedObject.polygon

          # If the points do not form a quad, find convex hull
          if len(points) > 4 : 
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
          else : 
            hull = points;

        # Number of points in the convex hull
          n = len(hull)     
          # Draw the convext hull
          for j in range(0,n):
            cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

          x = decodedObject.rect.left
          y = decodedObject.rect.top

          print(x, y)

          print('Type : ', decodedObject.type)
          print('Data : ', decodedObject.data,'\n')
          global val
          val=str(decodedObject.data)
          val=val[2:-1]
          print("Value is ",val)
          flag=1
          barCode = str(decodedObject.data)
          cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
      if(flag==1):
        break          
      # Display the resulting frame
      cv2.imshow('frame',frame)
      key = cv2.waitKey(1)
      if key & 0xFF == ord('q'):
          break
      elif key & 0xFF == ord('s'): # wait for 's' key to save 
          cv2.imwrite('Capture.png', frame)     

  print("QRCODE VALUE IS :",val)
  params = {
  'qrscannumber': val
  }
  r = requests.post(
    'http://127.0.0.1:5000/setQrScanNumber',
    data=params)
  cap.release()
  cv2.destroyAllWindows()


if __name__ == "__main__":
  print("Here hello")
  getandcheckqr()
  time.sleep(20)