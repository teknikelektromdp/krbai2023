#This is a python source code to detect the objects based on their contour and color i.e red rectangle and red hexagon
#import libraries
import cv2
import numpy as np
import imutils

#global variables
x_coordinates_rectangle = [];y_coordinates_rectangle = [];w_rectangle = [];h_rectangle = [];contour_rectangle = []
x_coordinates_hexagon = [];y_coordinates_hexagon = [];w_hexagon = [];h_hexagon = [];contour_hexagon = []

#capture video from webcam
vid = cv2.VideoCapture(1)

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def clearArray():
    x_coordinates_rectangle.clear()
    y_coordinates_rectangle.clear()
    w_rectangle.clear()
    h_rectangle.clear()
    contour_rectangle.clear()
    x_coordinates_hexagon.clear()
    y_coordinates_hexagon.clear()
    w_hexagon.clear()
    h_hexagon.clear()
    contour_hexagon.clear()
    
def objectDetection(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # red color 
    lower_red = np.array([0,100,100])
    upper_red = np.array([7,255,255])
    red = cv2.inRange(hsv, lower_red, upper_red)

    # using a findContours() function
    contours = cv2.findContours(
        red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    i = 0 
    # list for storing names of shapes
    for contour in contours:
    
        # here we are ignoring first counter because 
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue
    
        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
    
        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        #rectangle/square
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(contour)
            x_coordinates_rectangle.append(x)
            y_coordinates_rectangle.append(y)
            w_rectangle.append(w)
            h_rectangle.append(h)
            contour_rectangle.append(contour)
        
        #hexagon
        elif len(approx) == 6: 
            x,y,w,h = cv2.boundingRect(contour)
            x_coordinates_hexagon.append(x)
            y_coordinates_hexagon.append(y)
            w_hexagon.append(w)
            h_hexagon.append(h)
            contour_hexagon.append(contour)

    return x_coordinates_rectangle,y_coordinates_rectangle,w_rectangle,h_rectangle,contour_rectangle,x_coordinates_hexagon,y_coordinates_hexagon,w_hexagon,h_hexagon,contour_hexagon

while(True):

    #capture the video frame by frame
    ret, frame = vid.read()
    
    #adjust video resolution
    rescaled_video = rescale_frame(frame, percent=100)
    
    #red rectangle detector
    x_rectangle,y_rectangle,w_rectangle,h_rectangle,contour_rectangle,x_hexagon,y_hexagon,w_hexagon,h_hexagon,contour_hexagon = objectDetection(rescaled_video)
    if len(contour_rectangle) > 0:
        max_index_rectangle = np.array(w_rectangle).argmax()
        cv2.drawContours(rescaled_video, [contour_rectangle[max_index_rectangle]], 0, (0, 255, 0), 5)

    #red hexagon detector
    if len(contour_hexagon) > 0:
        max_index_hexagon = np.array(w_hexagon).argmax()
        cv2.drawContours(rescaled_video, [contour_hexagon[max_index_hexagon]], 0, (255, 0, 0), 5)

    #display the final frame
    cv2.imshow('KRBAI', rescaled_video)
    clearArray()

    if cv2.waitKey(1) &0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
