import PySimpleGUI as sg
import cv2
import numpy as np
import serial

def main():

    sg.theme('LightBlue')

    #define the menu bars
    menu_def = [['&Tools', ['&Serial Monitor', '&Soft Reset']], ]

    # define the window layout
    layout = [[sg.MenubarCustom(menu_def, pad=(0,0), k='-CUST MENUBAR-')],
              [sg.Text('Control Center', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Misi Wajib', size=(15, 1), font='Helvetica 12'),
               sg.Button('Misi Tambahan', size=(15, 1), font='Helvetica 12'),
               sg.Button('SOS', size=(15, 1), font='Helvetica 12'),
               sg.Button('Tombol Darurat', size=(15, 1), font='Helvetica 12'), ]]

    # create the window and show it without the plot
    window = sg.Window('Marine_Belido CC',
                       layout, element_justification='c', location=(800, 400), use_custom_titlebar=True)

    kernel = np.ones((5,5),np.uint8)
    #replace index with 0 or 1
    cap = cv2.VideoCapture(1)
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
    
    while True:
        
        #!--Do not remove
        #start the event
        event, values = window.read(timeout=0)
        #when user presses close button
        if event == sg.WIN_CLOSED:
            return
        elif event == 'Misi Wajib':
            sg.popup_auto_close('Please wait a few seconds...')
        elif event == 'Misi Tambahan':
            sg.popup_auto_close('Please wait a few seconds...')
        elif event == 'SOS':
            sg.popup_auto_close('Please wait a few seconds...')
        elif event == 'Tombol Darurat':
            sg.popup_auto_close('Please wait a few seconds...')
        elif event == 'Serial Monitor':
            sg.popup_no_titlebar('Under Maintenance')
        elif event == 'Soft Reset':
              sg.popup_no_titlebar('Under Maintenance')
        #Do not remove--!
        
        #!--Replace this part
        ##start of your main program
        ret, frame = cap.read()
        ##end of your main program
        #Replace this part--!

        #!--Do not remove
        #Do not add cv2.imshow as it's been declared here
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        window['image'].update(data=imgbytes)
        #Do not remove--!

        #This becomes unusable
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()