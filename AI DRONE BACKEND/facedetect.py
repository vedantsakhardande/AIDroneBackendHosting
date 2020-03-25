import numpy as np
import cv2
import math

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
cnt=0
len=0
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # ret, frame = cap.read() #read the data from the webcam
    
    facex=0
    facey=0
    facew=0
    faceh=0
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        facex=x
        facey=y
        facew=w
        faceh=h
        eyes = eye_cascade.detectMultiScale(roi_gray)
        cv2.imshow('img',img)
        len+=1
        print("Length=%d"%len)
        crop_img = img[facey:facey+faceh, facex:facex+facew]
        if(cnt<=len):
            cnt=cnt+1
            cv2.imshow("cropped", crop_img)
            cv2.waitKey(0)
            cv2.imwrite("img%d.jpeg"%cnt, crop_img) #code for saving frame into the file system
            print(cnt)
        else:
            break
        
    if(cv2.waitKey(1) & 0xFF == ord("q")): #wait key is the latency for which the program waits. Binding it to value q
        break
        # for (ex,ey,ew,eh) in eyes:
        #     # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #     x=int((ex+ex+ew)/2)
        #     y=int((ey+ey+eh)/2)
        #     rad=int((math.sqrt((eh*eh)+(ew*ew)))/2)
        #     cv2.circle(roi_color,(x,y),rad,(0,255,0),2)
        #     cv2.imshow('img',img)#image show module you can even put a random image in here
          
    
    # if(cv2.waitKey(1) & 0xFF == ord("c")): #wait key is the latency for which the program waits. Binding it to value c
        # ret, img = cap.read() #read the data from the webcam
      
            
        # cv2.imwrite("img%d.jpeg"%cnt, img) #code for saving frame into the file system
            # cv2.imwrite("img%d.jpeg"%cnt, crop_img) #code for saving frame into the file system
            # print(cnt)
            # cnt=cnt+1
            # if(cv2.waitKey(1) & 0xFF == ord("q")): #wait key is the latency for which the program waits. Binding it to value q
            #     break
        # cv2.imshow('img',img)
cap.release()
cv2.destroyAllWindows()