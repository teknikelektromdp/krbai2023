#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import serial
import time
import math

arduino = serial.Serial('/dev/ttyUSB1', 9600, timeout=.1)

kernel = np.ones((5,5),np.uint8)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
bola = 0
def nothing(x):
    pass

#membuat windows theresholding)
#membuat setingan maximum minimum warna
#membuat kernel maximum minimum


hthresh2 = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh2 = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh2 = cv2.inRange(np.array(20),np.array(75),np.array(255))

hthresh3 = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh3 = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh3 = cv2.inRange(np.array(20),np.array(75),np.array(255))
while(1):
    data = arduino.readline()
    print (data)
    radius=0
    ret, frame = cap.read()
    # Konversi frame ke mode HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)

    #cari

    hthresh3 = cv2.inRange(np.array(hue),np.array(160),np.array(170))
    sthresh3 = cv2.inRange(np.array(sat),np.array(50),np.array(255))
    vthresh3 = cv2.inRange(np.array(val),np.array(50),np.array(255))

    hthresh2 = cv2.inRange(np.array(hue),np.array(20),np.array(30))
    sthresh2 = cv2.inRange(np.array(sat),np.array(100),np.array(255))
    vthresh2 = cv2.inRange(np.array(val),np.array(100),np.array(255))

    tracking2 = cv2.bitwise_and(hthresh2,cv2.bitwise_and(sthresh2,vthresh2))
    tracking3 = cv2.bitwise_and(hthresh3,cv2.bitwise_and(sthresh3,vthresh3))

    dilation2 = cv2.dilate(tracking2,kernel,iterations = 1)
    dilation3 = cv2.dilate(tracking3,kernel,iterations = 1)
    th4 = cv2.morphologyEx(dilation2, cv2.MORPH_CLOSE, kernel)
    th5 = cv2.morphologyEx(dilation3, cv2.MORPH_CLOSE, kernel)
    closing2 = cv2.medianBlur(th4,5)
    closing3 = cv2.medianBlur(th5,5)
    moments = cv2.moments(closing)

    contours2 = cv2.findContours(closing2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours3 = cv2.findContours(closing3.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # Gambar area warna
    global x2,y2,x3,y3
    
    for contour in contours2:
        area = cv2.contourArea(contour)
        if area>800:
            (x2, y2), radius = cv2.minEnclosingCircle(contour)
            center = (int(x2), int(y2))
            radius = int(radius)
            x2 = int(x2)
            y2 = int(y2)
            cv2.circle(frame, center, radius, (0, 255, 0), 3)
            cv2.putText(frame, f"Yellow Circle {x2}, {y2}", (x2-20, y2-radius), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)
        
        posx=str(x2)
        posy=str(y2)
        arduino.write('x'.encode())
        arduino.write(posx.encode())
        arduino.write('\n'.encode())
        arduino.write('y'.encode())
        arduino.write(posy.encode())
        arduino.write('\n'.encode())
        
    for contour in contours3:
        area = cv2.contourArea(contour)
        if area>800:
            x3, y3, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x3,y3), (x3+w, y3+h), (173, 61, 255), 2)
            cv2.putText(frame, f"Magenta Square {x3}, {y3}", (x3,y3), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)

    cv2.imshow("Frame", frame)

    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()

