/*********************************************
 * Depth control and motion control for Underwater_ROV in sea levels
 * using pressure sensor MS5803 14B and IMU CMPS12
 * ali@mdp.ac.id
 * 
 * update Program 11 April 2023
 * IDE : Arduino 1.8.5
 * Hardware Platform : Arduino Pro Mega2560
 ********************************************/
#include <Wire.h>
#include <Servo.h>
#include "SparkFun_MS5803_I2C.h"
#include "I2Cdev.h"
#include "EEPROM.h"
#include "MPU6050.h"
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

//motor_dc control
//int inApin[4] = {22, 24, 26, 28};  // INA: Clockwise input
//int inBpin[4] = {23, 25, 27, 29}; // INB: Counter-clockwise input
//int pwmpin[4] = {5, 6, 7, 8}; // PWM input

int inApin[4] = {26, 28, 22, 24};  // INA: Clockwise input
int inBpin[4] = {27, 29, 23, 25}; // INB: Counter-clockwise input
int pwmpin[4] = {7, 8, 5, 6}; // PWM input

unsigned int suhu;
double pressure_abs;
double water_level;
volatile double set_level;
double reset_level = 0;
double avg;
double base_altitude = 1655.0; // Altitude of SparkFun's HQ in Boulder, CO. in (m)

//PID Library parameter
double de_Setpoint, de_Input, de_Output;
PID depth_PID(&de_Input, &de_Output, &de_Setpoint,6,2,1, DIRECT);
double Speed_ka = 0, Speed_ki = 0;
float depth_kp,depth_ki,depth_kd;

String inputString1 = "";
boolean mode = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
  //pressure sensor
  sensor.reset();
  sensor.begin();
  thrus_ka.attach(thrus_ka_pin);
  thrus_ki.attach(thrus_ki_pin);
  thrus_ka.writeMicroseconds(1500);
  thrus_ki.writeMicroseconds(1500);
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
  
  de_Setpoint = 0;
  de_Input =  pressure_abs;

  depth_PID.SetMode(AUTOMATIC);
  depth_PID.SetOutputLimits(-255,255);
  
//  depth_kp = EEPROM.read(4); depth_ki = EEPROM.read(5)*0.1;  depth_kd = EEPROM.read(6)*0.1;
  depth_kp = 10; depth_ki = 0; depth_kd = 0;
  Serial.print("Kp = "); Serial.print(depth_kp);
  Serial.print(", Ki = "); Serial.print(depth_ki);
  Serial.print(", Kd = "); Serial.print(depth_kd);

  pressure_abs = sensor.getPressure(ADC_1024);
  reset_level = pressure_abs;
  set_level = 100;
  delay(7000);
  Serial.print("OK_Ready!!!");
}

void loop() {
//  motorGo(1,cw,50);
//  motorGo(2,cw,50);
//  motorGo(3,cw,50);
//  thrus_ka.writeMicroseconds(1600);
//  thrus_ki.writeMicroseconds(1700);
  // put your main code here, to run repeatedly:
//  motorGo(0,cw,50);

  CMPS();
  
  suhu= sensor.getTemperature(CELSIUS, ADC_1024);     //read temperature from the sensor in celsius.
  pressure_abs = sensor.getPressure(ADC_1024);        // Read pressure from the sensor in mbar.
  myRA.addValue(pressure_abs);
  avg = myRA.getFastAverage();
  water_level = avg - reset_level;
  /*
  PID_Depth(depth_kp, depth_ki, depth_kd, avg);
  if(mode){
//    motorGo(0,de_Output>0?cw:ccw,abs(de_Output)); 
//    motorGo(1,de_Output>0?ccw:cw,abs(de_Output));
    thrus_ka.writeMicroseconds(1500);
    thrus_ki.writeMicroseconds(1500);
    Serial.print("kec : "); Serial.println(de_Output);
    if(water_level>80){
      
    }
  }
  else{
//    motorGo(0,cw,0); 
//    motorGo(1,cw,0);
    thrus_ka.writeMicroseconds(1500);
    thrus_ki.writeMicroseconds(1500);
  }
  */
  tampil();
}
