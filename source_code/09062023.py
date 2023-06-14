import cv2
import numpy as np

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
    x=0
    y=0
    radius=0
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)
    
    #cari
    hthresh = cv2.inRange(np.array(hue),np.array(0),np.array(20))
    sthresh = cv2.inRange(np.array(sat),np.array(100),np.array(255))
    vthresh = cv2.inRange(np.array(val),np.array(100),np.array(255))
    
    hthresh2 = cv2.inRange(np.array(hue),np.array(140),np.array(170))
    sthresh2 = cv2.inRange(np.array(sat),np.array(50),np.array(255))
    vthresh2 = cv2.inRange(np.array(val),np.array(50),np.array(255))
        
    hthresh3 = cv2.inRange(np.array(hue),np.array(20),np.array(30))
    sthresh3 = cv2.inRange(np.array(sat),np.array(100),np.array(255))
    vthresh3 = cv2.inRange(np.array(val),np.array(100),np.array(255))

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
            print("Red area coordinates: x=", x, "y=", y)
            
    for contour in contours2:
        area = cv2.contourArea(contour)
        corners = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if area > 500 and len(corners) > 7:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            x = int(x)
            y = int(y)
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            print("Yellow area coordinates: x=", x, "y=", y)
            
    for contour in contours3:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if area > 500 and len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.drawContours(frame, [contour], -1, (173, 61, 255), 2)
            print("Magenta area coordinates: x=", x, "y=", y)

    cv2.imshow("Frame", frame)

    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()