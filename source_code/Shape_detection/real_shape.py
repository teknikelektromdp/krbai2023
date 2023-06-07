import cv2
import numpy as np

def nothing(x):
    # any operation
    pass

tri = 0
rec = 0
pen = 0
hexa = 0
cir = 0

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 100, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    
    tri = 0
    rec = 0
    pen = 0
    hexa = 0
    cir = 0
    # Contours detection
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

            if len(approx) == 3:
                cv2.putText(frame, "Tri", (x, y), font, 1, (0, 0, 0))
                tri = tri + 1
            elif len(approx) == 4:
                cv2.putText(frame, "Recta", (x, y), font, 1, (0, 0, 0))
                rec = rec + 1
            elif len(approx) == 5:
                cv2.putText(frame, "Penta", (x, y), font, 1, (0, 0, 0))
                pen = pen + 1
            elif len(approx) == 6:
                cv2.putText(frame, "Hexa", (x, y), font, 1, (0, 0, 0))
                hexa = hexa + 1
            elif 6 < len(approx) < 20:
                cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
                cir = cir + 1

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    print("Triangle : ",tri)
    print("Rectangle : ",rec)
    print("Pentangle : ",pen)
    print("Hexangle :",hexa)
    print("Circle :",cir)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()