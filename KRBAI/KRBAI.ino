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

MS5803 sensor(ADDRESS_HIGH);      //ADDRESS_HIGH = 0x76 ;  ADDRESS_LOW  = 0x77

unsigned char high_byte, low_byte, angle8;
int pitch, roll, yaw;
unsigned int angle16;

//motor_dc control
int inApin[4] = {22, 24, 26, 28};  // INA: Clockwise input
int inBpin[4] = {23, 25, 27, 29}; // INB: Counter-clockwise input
int pwmpin[4] = {5, 6, 7, 8}; // PWM input

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
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
}

void loop() {
  // put your main code here, to run repeatedly:
  motorGo(0,cw,100);
  motorGo(1,cw,100);
  motorGo(2,cw,100);
  motorGo(3,cw,100);

  CMPS();
  tampil();
}
