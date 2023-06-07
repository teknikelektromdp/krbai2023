#Import Library OpenCV
import cv2

#Variable untuk VideoCapture
cap = cv2.VideoCapture(0)

#Fungsi untuk membuat frame pengaturan pada video
while(True):
    #Membaca video
    ret, frame = cap.read()
    #Menampilkan video
    cv2.imshow('frame',frame)
    #Pengaturan frame
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
