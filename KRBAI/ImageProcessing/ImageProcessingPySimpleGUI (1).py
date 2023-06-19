#!/usr/bin/env python
# coding: utf-8

# In[8]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import PySimpleGUI as sg
import requests

sg.theme("Reddit")
kernel = np.ones((5,5),np.uint8)
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
bola = 0
x1 = 0
x2 = 0
x3 = 0
y1 = 0
y2 = 0
y3 = 0
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
    hthresh3 = cv2.inRange(np.array(hue),np.array(120),np.array(130))
    sthresh3 = cv2.inRange(np.array(sat),np.array(50),np.array(255))
    vthresh3 = cv2.inRange(np.array(val),np.array(50),np.array(255))

    hthresh2 = cv2.inRange(np.array(hue),np.array(50),np.array(90))
    sthresh2 = cv2.inRange(np.array(sat),np.array(50),np.array(255))
    vthresh2 = cv2.inRange(np.array(val),np.array(50),np.array(255))

    tracking2 = cv2.bitwise_and(hthresh2,cv2.bitwise_and(sthresh2,vthresh2))
    tracking3 = cv2.bitwise_and(hthresh3,cv2.bitwise_and(sthresh3,vthresh3))

    dilation2 = cv2.dilate(tracking2,kernel,iterations = 1)
    dilation3 = cv2.dilate(tracking3,kernel,iterations = 1)
    th4 = cv2.morphologyEx(dilation2, cv2.MORPH_CLOSE, kernel)
    th5 = cv2.morphologyEx(dilation3, cv2.MORPH_CLOSE, kernel)
    closing2 = cv2.medianBlur(th4,5)
    closing3 = cv2.medianBlur(th5,5)

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
        
    for contour in contours3:
        area = cv2.contourArea(contour)
        if area>800:
            x3, y3, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x3,y3), (x3+w, y3+h), (173, 61, 255), 2)
            cv2.putText(frame, f"Magenta Square {x3}, {y3}", (x3,y3), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)

    return frame

def create_gui():
    col = [[sg.VPush()],
          [sg.Button(('Misi 1'), font='Comic 16 bold', size=(10,1)), sg.Button(('Misi 2'), font='Comic 16 bold', size=(10,1))],
          [sg.Push(), sg.Text('-', key='-MISI1-'), sg.Push(), sg.Text('-', key='-MISI2-'), sg.Push()],
          [sg.Button(('Lampu'), font='Comic 16 bold', size=(10,1)), sg.Button(('SOS'), font='Comic 16 bold', size=(10,1))],
          [sg.Push(), sg.Text('-', key='-LAMPU-'), sg.Push(), sg.Text('-', key='-SOS-'), sg.Push()],
          [sg.Button(('Stop'), font='Comic 16 bold', size=(21,1))],
          [sg.Push(), sg.Text('-', key='-STOP-'), sg.Push()],
          [sg.Text(('Pitch'), font=('Comic 18 bold'))],
          [sg.Text('KP'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KP1-')],
          [sg.Text('KI '), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KI1-')],
          [sg.Text('KD'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KD1-')],
          [sg.VPush()]
          ]
    
              
    col2 = [[sg.Text('SP_Depth'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(5,1)), sg.Button('✔️', key = '-SPD-')],
            [sg.Text('SP_Head '), sg.Spin([i for i in range(0,500)], initial_value=0, size=(5,1)), sg.Button('✔️', key = '-SPH-')],
            [sg.Text(('Depth'), font=('Comic 18 bold'))],
            [sg.Text('KP'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KP2-')],
            [sg.Text('KI '), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KI2-')],
            [sg.Text('KD'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KD2-')],
            [sg.Text(('Heading'), font=('Comic 18 bold')), sg.Push()],
            [sg.Text('KP'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KP3-'),sg.Push()],
            [sg.Text('KI '), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KI3-'),sg.Push()],
            [sg.Text('KD'), sg.Spin([i for i in range(0,500)], initial_value=0, size=(7,1)), sg.Button('✔️', key = '-KD3-'),sg.Push()]]
    
    layout = [[sg.VPush()],
                [sg.Push(), sg.Image(filename='', key='-IMAGE-'), sg.Column(col), sg.Column(col2), sg.Push()],
              [sg.VPush()]
             ]
   
             
    window = sg.Window('KRBAI', layout, resizable=True, finalize=True)
    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Misi 1":
            window['-MISI1-'].update('Execute misi 1')
        if event == "Misi 2":
            window['-MISI2-'].update('Execute misi 2')
        if event == "Lampu":
            window['-LAMPU-'].update('Execute lampu')
        if event == "SOS":
            window['-SOS-'].update('Execute sos')
        if event == "Stop":
            window['-STOP-'].update('Robot Berhenti')
            
        if event == "KP1":
            pass
        if event == "KP2":
            pass
        if event == "KP3":
            pass
        if event == "KI1":
            pass
        if event == "KI2":
            pass
        if event == "KI3":
            pass
        if event == "KD1":
            pass
        if event == "KD2":
            pass
        if event == "KD3":
            pass
        
        if event == "SPD":
            pass
        if event == "SPH":
            pass

        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            processed_frame = detect_color(frame)
            imgbytes = cv2.imencode('.png', processed_frame)[1].tobytes()
            window['-IMAGE-'].update(data=imgbytes)

    cap.release()
    window.close()

create_gui()

