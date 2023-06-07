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
#include <MS5803lib.h>
#include "I2Cdev.h"
//#include "EEPROM.h"
#include "KalmanFilter.h"
#include "PID_v1.h"
#include "RunningAverage.h"

#define cw    0
#define ccw   1
#define brake 2

#define CMPS12_ADDRESS 0x60  // Address of CMPS12 shifted right one bit for arduino wire library
#define ANGLE_8  1           // Register to read 8bit angle from

Servo thrus_ka;
Servo thrus_ki;
byte thrus_ka_pin = 9;
byte thrus_ki_pin = 10;

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

unsigned long startMillis;  
unsigned long currentMillis;
const unsigned long period = 60000;

String inputString1 = "";
boolean mode = false;
boolean head = false;
int state = HIGH;

int pixel_x, pixel_y;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
  //pressure sensor
  sensor.reset();
  sensor.begin();
  
  thrus_ka.attach(thrus_ka_pin);  thrus_ka.writeMicroseconds(1500);
  thrus_ki.attach(thrus_ki_pin);  thrus_ki.writeMicroseconds(1500);
  
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

  head_PID.SetMode(AUTOMATIC);
  head_PID.SetOutputLimits(-200,200);
  head_kp = 10; head_ki = 0; head_kd = 2;

  roll_PID.SetMode(AUTOMATIC);
  roll_PID.SetOutputLimits(-50,50);
  roll_kp = 10; roll_ki = 0; roll_kd = 0;
  
//  depth_kp = EEPROM.read(4); depth_ki = EEPROM.read(5)*0.1;  depth_kd = EEPROM.read(6)*0.1;
  depth_kp = 10; depth_ki = 0; depth_kd = 0;
  Serial.print("Kp = "); Serial.print(depth_kp);
  Serial.print(", Ki = "); Serial.print(depth_ki);
  Serial.print(", Kd = "); Serial.println(depth_kd);

  pressure_abs = sensor.getPressure(ADC_1024);
  reset_level = pressure_abs;
  set_level = 50;
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
  PID_Roll(roll_kp, roll_ki, roll_kd, yaw);
  
  currentMillis = millis();
  if (currentMillis - startMillis >= period){
    mode = false;
    head = false;
    set_level = 0;    
    startMillis = currentMillis;
    Serial.println("Mode Auto Misi Pertama Selesai");
  }
  
  if(mode){
//    motorGo(0,de_Output>0?cw:ccw,abs(de_Output)); 
//    motorGo(1,de_Output>0?ccw:cw,abs(de_Output));
    if(de_Output>0){
      thrus_ka.writeMicroseconds(1500 - abs(de_Output));
      thrus_ki.writeMicroseconds(1500 + abs(de_Output));
    }
    else if (de_Output<0){
      thrus_ka.writeMicroseconds(1500 + abs(de_Output));
      thrus_ki.writeMicroseconds(1500 - abs(de_Output));
    }
//    Serial.print("kec : "); Serial.println(de_Output);
//    if(water_level>80){
//      //motion
//    }
  }
  if(head){
    if(he_Output>10){
        rr_PID(abs(he_Output));
      }
    else if (he_Output<-10){
        lr_PID(abs(he_Output));
      }
//    Serial.print("kec : "); Serial.println(de_Output);
//    if(water_level>80){
//      //motion
//    }
    else{
        forward();
      } 
    }
    
  else{
//      berhenti();
  } 
  tampil();
}
