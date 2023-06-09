import cv2
import math
import numpy as np
import serial
import time
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
kernel = np.ones((5,5),np.uint8)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
bola = 0
def nothing(x):
    pass

#membuat layar maximumum minimum warna
cv2.namedWindow('minimum')
cv2.namedWindow('maximum')

#membuat windows theresholding)
#membuat setingan maximum minimum warna
#membuat kernel maximum minimum
img = np.zeros((300,512,3), np.uint8)
img1 = np.zeros((300,512,3), np.uint8)

cv2.createTrackbar('hmin', 'minimum',0,255,nothing)
cv2.createTrackbar('hmax', 'maximum',74,255,nothing)

cv2.createTrackbar('smin', 'minimum',136,255,nothing)
cv2.createTrackbar('smax', 'maximum',255,255,nothing)

cv2.createTrackbar('vmin', 'minimum',103,255,nothing)
cv2.createTrackbar('vmax', 'maximum',218,255,nothing)

hthresh = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh = cv2.inRange(np.array(20),np.array(75),np.array(255))
while(1):
    data = arduino.readline()
    print (data )
    x=0
    y=0
    radius=0
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)

   
    hmn = cv2.getTrackbarPos('hmin','minimum')
    hmx = cv2.getTrackbarPos('hmax','maximum')
    
    smn = cv2.getTrackbarPos('smin','minimum')
    smx = cv2.getTrackbarPos('smax','maximum')

    vmn = cv2.getTrackbarPos('vmin','minimum')
    vmx = cv2.getTrackbarPos('vmax','maximum')

   
    img[:] = [hmn,smn,vmn]
    img1[:] = [hmx,smx,vmx]
    
    #cari
    hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
    sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
    vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
    
    dilation = cv2.dilate(tracking,kernel,iterations = 1)
    th3 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.medianBlur(th3,5)
    moments = cv2.moments(closing)
    
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    	
    if len(cnts) > 0:
            z = int(moments['m10']/moments['m00'])
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            else:
                center = 0, 0
		
            if radius > 10:			
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 10)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                cv2.putText(frame, "Tengah", (center[0] + 10, center[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                cv2.putText(frame, "(" + str(center[0]) + "," + str(center[1]) + ")", (center[0] + 10, center[1] + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                nilaiX=int(x)
                nilaiY=int(y)
                posx=str(nilaiX)
                posy=str(nilaiY)
#                print (posx,posy)
                arduino.write('X'.encode())
                arduino.write(posx.encode())
                arduino.write('\n'.encode())
    else :
                nilaiX=int(0)
                nilaiY=int(0)
                posx=str(nilaiX)
                posy=str(nilaiY)
      #          print (posx,posy)
                
	
    cv2.imshow('minimum' ,img)
    cv2.imshow('maximum' ,img1)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", closing)

    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        arduino.close()
        break

cap.release()

cv2.destroyAllWindows()
