# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:29:21 2023

@author: ali_zainal
"""

import cv2
import numpy as np
import serial
import time
import math

##arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)

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
cv2.namedWindow('minimum2')
cv2.namedWindow('maximum2')
cv2.namedWindow('minimum3')
cv2.namedWindow('maximum3')

#membuat windows theresholding)
#membuat setingan maximum minimum warna
#membuat kernel maximum minimum

cv2.createTrackbar('hmin', 'minimum',0,255,nothing)
cv2.createTrackbar('hmax', 'maximum',20,255,nothing)

cv2.createTrackbar('smin', 'minimum',100,255,nothing)
cv2.createTrackbar('smax', 'maximum',255,255,nothing)

cv2.createTrackbar('vmin', 'minimum',100,255,nothing)
cv2.createTrackbar('vmax', 'maximum',255,255,nothing)

cv2.createTrackbar('hmin3', 'minimum3',140,255,nothing)
cv2.createTrackbar('hmax3', 'maximum3',170,255,nothing)

cv2.createTrackbar('smin3', 'minimum3',50,255,nothing)
cv2.createTrackbar('smax3', 'maximum3',255,255,nothing)

cv2.createTrackbar('vmin3', 'minimum3',50,255,nothing)
cv2.createTrackbar('vmax3', 'maximum3',255,255,nothing)

cv2.createTrackbar('hmin2', 'minimum2',20,255,nothing)
cv2.createTrackbar('hmax2', 'maximum2',30,255,nothing)

cv2.createTrackbar('smin2', 'minimum2',100,255,nothing)
cv2.createTrackbar('smax2', 'maximum2',255,255,nothing)

cv2.createTrackbar('vmin2', 'minimum2',100,255,nothing)
cv2.createTrackbar('vmax2', 'maximum2',255,255,nothing)


hthresh = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh = cv2.inRange(np.array(20),np.array(75),np.array(255))

hthresh2 = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh2 = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh2 = cv2.inRange(np.array(20),np.array(75),np.array(255))

hthresh3 = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh3 = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh3 = cv2.inRange(np.array(20),np.array(75),np.array(255))
while(1):
##    data = arduino.readline()
##    print (data)
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

    hmn2 = cv2.getTrackbarPos('hmin2','minimum2')
    hmx2 = cv2.getTrackbarPos('hmax2','maximum2')

    smn2 = cv2.getTrackbarPos('smin2','minimum2')
    smx2 = cv2.getTrackbarPos('smax2','maximum2')

    vmn2 = cv2.getTrackbarPos('vmin2','minimum2')
    vmx2 = cv2.getTrackbarPos('vmax2','maximum2')

    hmn3 = cv2.getTrackbarPos('hmin3','minimum3')
    hmx3 = cv2.getTrackbarPos('hmax3','maximum3')
    
    smn3 = cv2.getTrackbarPos('smin3','minimum3')
    smx3 = cv2.getTrackbarPos('smax3','maximum3')

    vmn3 = cv2.getTrackbarPos('vmin3','minimum3')
    vmx3 = cv2.getTrackbarPos('vmax3','maximum3')

    #cari
    hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
    sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
    vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

    hthresh2 = cv2.inRange(np.array(hue),np.array(hmn2),np.array(hmx2))
    sthresh2 = cv2.inRange(np.array(sat),np.array(smn2),np.array(smx2))
    vthresh2 = cv2.inRange(np.array(val),np.array(vmn2),np.array(vmx2))

    hthresh3 = cv2.inRange(np.array(hue),np.array(hmn3),np.array(hmx3))
    sthresh3 = cv2.inRange(np.array(sat),np.array(smn3),np.array(smx3))
    vthresh3 = cv2.inRange(np.array(val),np.array(vmn3),np.array(vmx3))

    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
    tracking2 = cv2.bitwise_and(hthresh2,cv2.bitwise_and(sthresh2,vthresh2))
    tracking3 = cv2.bitwise_and(hthresh3,cv2.bitwise_and(sthresh3,vthresh3))

    dilation = cv2.dilate(tracking,kernel,iterations = 1)
    dilation2 = cv2.dilate(tracking2,kernel,iterations = 1)
    dilation3 = cv2.dilate(tracking3,kernel,iterations = 1)
    th3 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    th4 = cv2.morphologyEx(dilation2, cv2.MORPH_CLOSE, kernel)
    th5 = cv2.morphologyEx(dilation3, cv2.MORPH_CLOSE, kernel)
    closing = cv2.medianBlur(th3,5)
    closing2 = cv2.medianBlur(th4,5)
    closing3 = cv2.medianBlur(th5,5)
    moments = cv2.moments(closing)

    contours = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours2 = cv2.findContours(closing2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours3 = cv2.findContours(closing3.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if area > 500 and len(approx) == 3:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
##            print("Red area coordinates: x=", x, "y=", y)

    for contour in contours2:
        area = cv2.contourArea(contour)
        corners = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if area > 500 and len(corners) > 7:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            x = int(x)
            y = int(y)
            cv2.circle(frame, center, radius, (255, 255, 0), 2)
##            print("Yellow area coordinates: x=", x, "y=", y)

    for contour in contours3:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if area > 500 and len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.drawContours(frame, [contour], -1, (173, 61, 255), 2)
##            print("Magenta area coordinates: x=", x, "y=", y)

            posx=str(x)
            posy=str(y)
##            print (posx,posy)
            
##            arduino.write('x'.encode())
##            arduino.write(posx.encode())
##            arduino.write('\n'.encode())
##            arduino.write('y'.encode())
##            arduino.write(posy.encode())
##            arduino.write('\n'.encode())

    cv2.imshow("Frame", frame)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
