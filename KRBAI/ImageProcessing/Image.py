#pip install flet
import flet as ft
import base64
import numpy as np
import cv2

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
class Countdown(ft.UserControl):
    
    def __init__(self):
        super().__init__()

    def did_mount(self):
        self.update_timer()

    def update_timer(self):
        while True:
            ret, frame = cap.read()
            # Konversi frame ke mode HSV
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
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
                    
            ret, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = im_b64.decode("utf-8")
            self.update()


    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        return self.img

def height_changed(e):
    print(e.control.value)

    
class Refresh(ft.UserControl):
    def refresh_click(self, e):
        global x1,x2,y1,y2,x3,y3
        self.counter = f"Segitiga merah {x1}, {y1} \nLingkaran Kuning {x2}, {y2} \nPersegi Magenta {x3}, {y3}"
        self.text.value = str(self.counter)
        self.update()

    def build(self):
        self.counter = 0
        self.text = ft.Text(str(self.counter))
        return ft.Row([self.text, ft.ElevatedButton("Refresh", on_click=self.refresh_click)])
        

def main(page: ft.Page):
    page.title = "KRBAI 🤖"
    page.padding = 30
    page.alignment = ft.alignment.center
    page.window_left = page.window_left+100
    page.theme_mode = ft.ThemeMode.LIGHT
    
    txt_number1 = ft.TextField(value="0", text_align="right", width=60)
    txt_number2 = ft.TextField(value="0", text_align="right", width=60)
    txt_number3 = ft.TextField(value="0", text_align="right", width=60)
    txt_number4 = ft.TextField(value="0", text_align="right", width=60)
    txt_number5 = ft.TextField(value="0", text_align="right", width=60)
    txt_number6 = ft.TextField(value="0", text_align="right", width=60)
    txt_number7 = ft.TextField(value="0", text_align="right", width=60)
    txt_number8 = ft.TextField(value="0", text_align="right", width=60)
    txt_number9 = ft.TextField(value="0", text_align="right", width=60)
    txt_numberx = ft.TextField(value="0", text_align="right", width=60)
    txt_numbery = ft.TextField(value="0", text_align="right", width=60)
    mission1 = ft.Text("-")
    mission2 = ft.Text("-")
    textLampu = ft.Text("-")
    textSos = ft.Text("-")
    textStop = ft.Text("-")
    
    def misi1(e):
        mission1.value="Execute Misi 1"
        page.update()
        
    def misi2(e):
        mission2.value="Execute Misi 2"
        page.update()
        
    def lampu(e):
        textLampu.value="Execute Lampu"
        page.update()
        
    def sos(e):
        textSos.value="Execute SOS"
        page.update()
        
    def stop(e):
        textStop.value="Robot Berhenti"
        page.update()
        
    def minus_click(variable):
        variable.value = str(int(variable.value) - 1)
        page.update()

    def plus_click(variable):
        variable.value = str(int(variable.value) + 1)
        page.update()
        
    def sp_depth(e):
        pass
    def sp_head(e):
        pass
    def depth_kp(e):
        pass
    def depth_ki(e):
        pass
    def depth_kd(e):
        pass
    def head_kp(e):
        pass
    def head_ki(e):
        pass
    def head_kd(e):
        pass
    def pitch_kp(e):
        pass
    def pitch_ki(e):
        pass
    def pitch_kd(e):
        pass
        
    section = ft.Container(
        margin=ft.margin.only(right=100),
        content=ft.Row([
            ft.Column([
                ft.Container(
                    ft.Image(
                    src=f"https://cdn.discordapp.com/attachments/948199395072016454/1118090728984301628/MDP.png",
                    width=100,
                    height=60,
                    fit=ft.ImageFit.COVER), margin=ft.margin.only(left=320),
                ),
                ft.Card(
                    content=ft.Container(
                        bgcolor=ft.colors.RED_900,
                        padding=10,
                        border_radius = ft.border_radius.all(20),
                        content=ft.Column([
                            Countdown(),
                            ft.Text("OBJECT DETECTION",
                                 size=20, weight="bold",
                                 color=ft.colors.WHITE),
                        ]
                        ),
                    )
                ),
                
            ],alignment=ft.MainAxisAlignment.CENTER,),
            
            ft.Container(
                ft.Column([
                    
                    ft.Row([
                        ft.Column([
                            ft.Container(
                                content=ft.Text("MISI 1", weight="bold", color=ft.colors.WHITE),
                                padding=5,
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.RED_700,
                                width=100,
                                height=30,
                                border_radius=10,
                                ink=True,
                                on_click=misi1,
                            ),
                            mission1,
                        ]),
                        ft.Column([
                            ft.Container(
                                content=ft.Text("MISI 2", weight="bold", color=ft.colors.WHITE),
                                padding=5,
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.RED_700,
                                width=100,
                                height=30,
                                border_radius=10,
                                ink=True,
                                on_click=misi2,
                            ),
                            mission2,
                        ])
                    ]),
                    ft.Row([
                        ft.Column([
                            ft.Container(
                                content=ft.Text("Lampu", weight="bold", color=ft.colors.WHITE),
                                padding=5,
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.RED_700,
                                width=100,
                                height=30,
                                border_radius=10,
                                ink=True,
                                on_click=lampu,
                            ),
                            textLampu,
                        ]),
                        ft.Column([
                            ft.Container(
                                content=ft.Text("SOS", weight="bold", color=ft.colors.WHITE),
                                padding=5,
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.RED_700,
                                width=100,
                                height=30,
                                border_radius=10,
                                ink=True,
                                on_click=sos,
                            ),
                            textSos,
                        ])
                    ]),
                    
                
                    ft.Row([
                        ft.Text("SP_Depth"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_numberx)),
                        txt_numberx,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_numberx)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=sp_depth),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("SP_Head "),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_numbery)),
                        txt_numbery,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_numbery)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=sp_head),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Text(
                        "Pitch",
                        style= ft.TextThemeStyle.TITLE_MEDIUM,
                        weight="bold"
                    ),
                    ft.Row([
                        ft.Text("KP"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number1)),
                        txt_number1,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number1)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=pitch_kp),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("KI "),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number2)),
                        txt_number2,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number2)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=pitch_ki),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("KD"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number3)),
                        txt_number3,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number3)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=pitch_kd),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                ]),
                
                
            ), 
            
            ft.Container(
                ft.Column([
                    ft.Text(
                        "Depth",
                        style= ft.TextThemeStyle.TITLE_MEDIUM,
                        weight="bold",
                    ),
                    ft.Row([
                        ft.Text("KP"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number4)),
                        txt_number4,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number4)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=depth_kp),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("KI "),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number5)),
                        txt_number5,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number5)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=depth_ki),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("KD"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number6)),
                        txt_number6,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number6)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=depth_kd),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Text(
                        "Heading",
                        style= ft.TextThemeStyle.TITLE_MEDIUM,
                        weight="bold"
                    ),
                    ft.Row([
                        ft.Text("KP"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number7)),
                        txt_number7,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number7)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=head_kp),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("KI "),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number8)),
                        txt_number8,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number8)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=head_ki),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    
                    ft.Row([
                        ft.Text("KD"),
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click(txt_number9)),
                        txt_number9,
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: plus_click(txt_number9)),
                        ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=head_kd),
                    ],alignment=ft.MainAxisAlignment.CENTER,),
                    ft.Column([
                        ft.Container(
                            content=ft.Text("STOP", weight="bold", color=ft.colors.WHITE),
                            padding=5,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.RED_700,
                            width=230,
                            height=40,
                            border_radius=10,
                            ink=True,
                            on_click=stop,
                        ),
                        textStop,
                    ]),
                ]),
                    
            ),
        
        ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

        
    page.add(
        section,
    )

if __name__ == '__main__':
    ft.app(target=main)
    #ft.app(target=main,view=ft.WEB_BROWSER)
    cap.release()
    cv2.destroyAllWindows()
