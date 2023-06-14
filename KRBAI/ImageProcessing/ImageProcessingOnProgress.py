#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
import PySimpleGUI as sg

kernel = np.ones((5,5),np.uint8)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
bola = 0
x1 = 0
x2 = 0
x3 = 0
y1 = 0
y2 = 0
y3 = 0
hthresh = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh = cv2.inRange(np.array(20),np.array(75),np.array(255))

hthresh2 = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh2 = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh2 = cv2.inRange(np.array(20),np.array(75),np.array(255))

hthresh3 = cv2.inRange(np.array(20),np.array(111),np.array(173))
sthresh3 = cv2.inRange(np.array(39),np.array(58),np.array(87))
vthresh3 = cv2.inRange(np.array(20),np.array(75),np.array(255))
def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)

    #cari
    hthresh = cv2.inRange(np.array(hue),np.array(0),np.array(10))
    sthresh = cv2.inRange(np.array(sat),np.array(100),np.array(255))
    vthresh = cv2.inRange(np.array(val),np.array(100),np.array(255))

    hthresh3 = cv2.inRange(np.array(hue),np.array(140),np.array(170))
    sthresh3 = cv2.inRange(np.array(sat),np.array(50),np.array(255))
    vthresh3 = cv2.inRange(np.array(val),np.array(50),np.array(255))

    hthresh2 = cv2.inRange(np.array(hue),np.array(20),np.array(30))
    sthresh2 = cv2.inRange(np.array(sat),np.array(100),np.array(255))
    vthresh2 = cv2.inRange(np.array(val),np.array(100),np.array(255))

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
    # Gambar area warna
    global x1,y1,x2,y2,x3,y3
    largest_triangle= None
    largest_circle= None
    largest_square= None
    largest_area1 = 0
    largest_area2 = 0
    largest_area3 = 0
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        area = cv2.contourArea(contour)
        if len(approx) == 3 and area>500:
            if area > largest_area1:
                largest_area1 = area
                largest_triangle = contour

    if largest_triangle is not None:
        x1, y1, w, h = cv2.boundingRect(largest_triangle)
        cv2.drawContours(frame, [largest_triangle], -1, (0, 0, 255), 3)
        cv2.putText(frame, f"Red Triangle {x1}, {y1}", (x1-20,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)


    for contour in contours2:
        corners = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if len(corners) > 7 and area>500:
            if area > largest_area2:
                largest_area2 = area
                largest_circle = contour

    if largest_circle is not None:
        (x2, y2), radius = cv2.minEnclosingCircle(contour)
        center = (int(x2), int(y2))
        radius = int(radius)
        x2 = int(x2)
        y2 = int(y2)
        cv2.circle(frame, center, radius, (0, 255, 0), 3)
        cv2.putText(frame, f"Yellow Circle {x2}, {y2}", (x2-20, y2-radius), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)

    for contour in contours3:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        area = cv2.contourArea(contour)
        if len(approx) == 4 and area>500:
            if area > largest_area3:
                largest_area3 = area
                largest_square = contour

    if largest_square is not None:
        x3, y3, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x3,y3), (x3+w, y3+h), (173, 61, 255), 2)
        cv2.putText(frame, f"Magenta Square {x3}, {y3}", (x3,y3), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)

    return frame

# Fungsi untuk membuat GUI
def create_gui():
    layout = [[sg.Image(filename='', key='-IMAGE-')],
             [sg.Button('Misi 1')],
             [sg.Spin([i for i in range(0,500)], initial_value=0), sg.Text('KP')],
             [sg.Spin([i for i in range(0,500)], initial_value=0), sg.Text('KI')],
             [sg.Spin([i for i in range(0,500)], initial_value=0), sg.Text('KD')]]
    window = sg.Window('Real-Time Color Detection', layout, resizable=True, finalize=True)
    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == sg.WINDOW_CLOSED:
            break

        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            processed_frame = detect_color(frame)
            imgbytes = cv2.imencode('.png', processed_frame)[1].tobytes()
            window['-IMAGE-'].update(data=imgbytes)

    cap.release()
    window.close()

# Jalankan program
create_gui()


# In[1]:




