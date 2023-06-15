/*********************************************
 * Depth control and motion control for Underwater_ROV in sea levels
 * using pressure sensor MS5803 14B and IMU CMPS12
 * ali@mdp.ac.id
 * 
 * update Program 09 Mei 2023
 * IDE : Arduino 1.8.5
 * Hardware Platform : Arduino Pro Mega2560
 ********************************************/
#include <Wire.h>
#include <Servo.h>
#include <MS5803.h>
#include "I2Cdev.h"
#include "EEPROM.h"
//#include "KalmanFilter.h"
#include "PID_v1.h"
#include "RunningAverage.h"

#define cw    0
#define ccw   1
#define brake 2

#define CMPS12_ADDRESS 0x60  // Address of CMPS12 shifted right one bit for arduino wire library
#define ANGLE_8  1           // Register to read 8bit angle from

Servo thrus_ka;
Servo thrus_ki;
Servo thrus_pi;
Servo thrus_1;
Servo thrus_2;
Servo thrus_3;
Servo thrus_4;

byte thrus_ka_pin = 7;
byte thrus_ki_pin = 8;
byte thrus_pi_pin = 9;
byte thrus_1_pin = 10;
byte thrus_2_pin = 11;
byte thrus_3_pin = 16;
byte thrus_4_pin = 12;

RunningAverage myRA(10);

MS5803 sensor(ADDRESS_HIGH);      //ADDRESS_HIGH = 0x76 ;  ADDRESS_LOW  = 0x77

unsigned char high_byte, low_byte, angle8;
int pitch, roll, yaw;
unsigned int angle16;

int inApin[4] = {26, 28, 22, 24};  // INA: Clockwise input
int inBpin[4] = {27, 29, 23, 25}; // INB: Counter-clockwise input
int pwmpin[4] = {7, 8, 5, 6}; // PWM input

unsigned int suhu;
double pressure_abs;
double water_level;
volatile double set_level;
volatile double set_head;
double reset_level = 0;
double avg;
double base_altitude = 1655.0; // Altitude of SparkFun's HQ in Boulder, CO. in (m)

//PID Library parameter
double de_Setpoint, de_Input, de_Output;
float depth_kp,depth_ki,depth_kd;
PID depth_PID(&de_Input, &de_Output, &de_Setpoint,depth_kp,depth_ki,depth_kd, DIRECT);

//PID Heading
double he_Setpoint, he_Input, he_Output;
float head_kp,head_ki,head_kd;
PID head_PID(&he_Input, &he_Output, &he_Setpoint,head_kp,head_ki,head_kd, DIRECT);

//PID ROll
double ro_Setpoint, ro_Input, ro_Output;
float roll_kp,roll_ki,roll_kd;
PID roll_PID(&ro_Input, &ro_Output, &ro_Setpoint,roll_kp,roll_ki,roll_kd, DIRECT);

//PID Pitch
double pi_Setpoint, pi_Input, pi_Output;
float pitch_kp,pitch_ki,pitch_kd;
PID pitch_PID(&pi_Input, &pi_Output, &pi_Setpoint,pitch_kp,pitch_ki,pitch_kd, DIRECT);

unsigned long startMillis;  
unsigned long currentMillis;
const unsigned long period = 80000;   //periode lama menyelam

String inputString1 = "";
String inputString2 = "";
boolean mode = false;
boolean head = true;
boolean misi = false;
boolean misi2 = false;
<<<<<<< HEAD
boolean objek = false;
boolean pitch_status = false;
=======
boolean pitch_status = true;
>>>>>>> 1609fa56b7f6c489d4208730e847c919b41e6b39
int state = HIGH;

int pixel_x, pixel_y;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  Wire.begin();
  //pressure sensor
  sensor.reset();
  sensor.begin();
  
  thrus_ka.attach(thrus_ka_pin);  thrus_ka.writeMicroseconds(1500);
  thrus_ki.attach(thrus_ki_pin);  thrus_ki.writeMicroseconds(1500);
  thrus_pi.attach(thrus_pi_pin);  thrus_pi.writeMicroseconds(1500);
  thrus_1.attach(thrus_1_pin);  thrus_1.writeMicroseconds(1500);
  thrus_2.attach(thrus_2_pin);  thrus_2.writeMicroseconds(1500);
  thrus_3.attach(thrus_3_pin);  thrus_3.writeMicroseconds(1500);
  thrus_4.attach(thrus_4_pin);  thrus_4.writeMicroseconds(1500);
  
  for (int i=0; i<7; i++)
  {
    pinMode(inApin[i], OUTPUT);
    pinMode(inBpin[i], OUTPUT);
    pinMode(pwmpin[i], OUTPUT);
  }
  // Initialize braked
  for (int i=0; i<7; i++)
  {
    digitalWrite(inApin[i], LOW);
    digitalWrite(inBpin[i], LOW);
  }
  pinMode(46, OUTPUT); pinMode(47, OUTPUT);
  digitalWrite(46, HIGH); digitalWrite(47, HIGH);
  
  de_Setpoint = 0;
  de_Input =  pressure_abs;

  depth_PID.SetMode(AUTOMATIC);
  depth_PID.SetOutputLimits(-200,200);
  depth_kp = 20; depth_ki = 0; depth_kd = 0;
//  depth_kp = EEPROM.read(2); depth_ki = EEPROM.read(3)*0.1;  depth_kd = EEPROM.read(4)*0.1;
  
  head_PID.SetMode(AUTOMATIC);
  head_PID.SetOutputLimits(-200,200);
  head_kp = 10; head_ki = 0; head_kd = 2;
<<<<<<< HEAD
  head_kp = EEPROM.read(5); head_ki = EEPROM.read(6)*0.1;  head_kd = EEPROM.read(7)*0.1;
=======
//  head_kp = EEPROM.read(5); head_ki = EEPROM.read(6)*0.1; head_kd = EEPROM.read(7)*0.1;
>>>>>>> 1609fa56b7f6c489d4208730e847c919b41e6b39
  
  roll_PID.SetMode(AUTOMATIC);
  roll_PID.SetOutputLimits(-50,50);
  roll_kp = 10; roll_ki = 0; roll_kd = 0;

  pitch_PID.SetMode(AUTOMATIC);
  pitch_PID.SetOutputLimits(-200,200);
  pitch_kp = 10; pitch_ki = 0; pitch_kd = 2;
  
//  depth_kp = EEPROM.read(4); depth_ki = EEPROM.read(5)*0.1;  depth_kd = EEPROM.read(6)*0.1;
  Serial.print("Kp = "); Serial.print(depth_kp);
  Serial.print(", Ki = "); Serial.print(depth_ki);
  Serial.print(", Kd = "); Serial.println(depth_kd);

  pressure_abs = sensor.getPressure(ADC_1024);
  reset_level = pressure_abs;
  set_level = 50;
//  set_level = EEPROM.read(1);
  CMPS();
  set_head = yaw;
  Serial.print("Set Point depth = ");Serial.println(set_level);
  Serial.print("Set Point Heading = ");Serial.println(set_head);
  delay(7000);
  startMillis = millis();
  Serial.println("OK_Ready!!!");
}

void loop() {
//  thrus_ka.writeMicroseconds(1600);
//  thrus_ki.writeMicroseconds(1700);
  // put your main code here, to run repeatedly:
  CMPS();
  suhu= sensor.getTemperature(CELSIUS, ADC_1024);     //read temperature from the sensor in celsius.
  pressure_abs = sensor.getPressure(ADC_1024);        // Read pressure from the sensor in mbar.
  myRA.addValue(pressure_abs);
  avg = myRA.getFastAverage();
  water_level = avg - reset_level;
  
  PID_Depth(depth_kp, depth_ki, depth_kd, avg);
  PID_Heading(head_kp, head_ki, head_kd, yaw);
  PID_Roll(roll_kp, roll_ki, roll_kd, roll);
  PID_pitch(pitch_kp, pitch_ki, pitch_kd, pitch);

  //misi utama berdasarkan waktu
  currentMillis = millis();
  if(misi){
    set_level = 50;
    mode = true;
    head = true;
    if (currentMillis - startMillis >= period){
//      mode = false;
      head = false;
      set_level = 0;    
      startMillis = currentMillis;
      Serial.println("Mode Auto Misi Pertama Selesai");
    }
  }

  //Misi tambahan image pro
  if(misi2){
    set_level = 50;
    mode = true;
    head = true;
  }

  //depth control
  if(mode){
//    motorGo(0,de_Output>0?cw:ccw,abs(de_Output)); 
//    motorGo(1,de_Output>0?ccw:cw,abs(de_Output));
    if(de_Output<0){
      thrus_ka.writeMicroseconds(1500 - abs(de_Output));
      thrus_ki.writeMicroseconds(1500 + abs(de_Output));
    }
    else if (de_Output>0){
      thrus_ka.writeMicroseconds(1500 + abs(de_Output));
      thrus_ki.writeMicroseconds(1500 - abs(de_Output));
    }
//    Serial.print("kec : "); Serial.println(de_Output);
//    if(water_level>80){
//      //motion
//    }
  }
  Serial.print("kec : "); Serial.println(he_Output);
  //heading control
  if(head){
<<<<<<< HEAD
    if(he_Output>30){
        rr_PID(abs(he_Output));
    }
    else if (he_Output<-30){
        lr_PID(abs(he_Output));
    }
//    
=======
    if(set_head > set_head-5){
        lr_PID(abs(he_Output));
    }
    else if (set_head < set_head+5){
        rr_PID(abs(he_Output));
    }
>>>>>>> 1609fa56b7f6c489d4208730e847c919b41e6b39
//    if(water_level>80){
//      //motion
//    }
    else{
        forward();
    } 
    Serial.print("kec : "); Serial.println(he_Output);
  }
    
  //pitch control
  if(pitch_status){
    if(pi_Output>0){
      thrus_pi.writeMicroseconds(1500 - abs(pi_Output));
    }
    else if (pi_Output<0){
      thrus_pi.writeMicroseconds(1500 + abs(pi_Output));
    }
  }
  
  //left pixel_x set point = 320
  if(objek){
    if(pixel_x>330 && pixel_x<640){
      shift_right1(100);
    }
    else if (pixel_x>0 && pixel_x<310){
      shift_left1(100);
    }
    else{
      berhenti();
    }
  }
    
  else{
//      berhenti();
  }
  tampil();
  
}
