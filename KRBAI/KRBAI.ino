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

unsigned char high_byte, low_byte, angle8;
char pitch, roll;
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

  Wire.beginTransmission(CMPS12_ADDRESS);  //starts communication with CMPS12
  Wire.write(ANGLE_8);                     //Sends the register we wish to start reading from
  Wire.endTransmission();
 
  // Request 5 bytes from the CMPS12
  // this will give us the 8 bit bearing, 
  // both bytes of the 16 bit bearing, pitch and roll
  Wire.requestFrom(CMPS12_ADDRESS, 5);       
  
  while(Wire.available() < 5);        // Wait for all bytes to come back
  
  angle8 = Wire.read();               // Read back the 5 bytes
  high_byte = Wire.read();
  low_byte = Wire.read();
  pitch = Wire.read();
  roll = Wire.read();
  
  angle16 = high_byte;                 // Calculate 16 bit angle
  angle16 <<= 8;
  angle16 += low_byte;
    
  Serial.print("roll: ");               // Display roll data
  Serial.print(roll, DEC);
  
  Serial.print("    pitch: ");          // Display pitch data
  Serial.print(pitch, DEC);
  
  Serial.print("    angle full: ");     // Display 16 bit angle with decimal place
  Serial.print(angle16 / 10, DEC);
  Serial.print(".");
  Serial.print(angle16 % 10, DEC);
  
  Serial.print("    angle 8: ");        // Display 8bit angle
  Serial.println(angle8, DEC);
  
  delay(100);                           // Short delay before next loop

}
