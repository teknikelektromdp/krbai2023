void tampil(){
  Serial.print("roll: ");             Serial.print(roll);
  Serial.print("    pitch: ");        Serial.print(pitch);
  Serial.print("    Yaw (angle): ");  Serial.println(yaw);

  Serial.print("SP_depth (cm): ");    Serial.print(set_level);
  Serial.print(", set_point: ");        Serial.print(de_Setpoint);
  Serial.print(", Pressure: ");       Serial.print(avg);
  Serial.print(", water_lvl: ");      Serial.println(water_level);
  
  delay(100);
}

void serialEvent() {
   while (Serial.available()) {
     char inChar = (char)Serial.read();
     inputString1 += inChar;
     if (inChar == '\n') {
      if(inputString1.substring(0,1)=="x"){
//        pixel_x =inputString1.substring(1).toInt();
      }
      else if(inputString1.substring(0,1)=="y"){
//        pixel_y =inputString1.substring(1).toInt();
      }
      else if(inputString1=="stop\n"){
          motorGo(0,cw,0);motorGo(1,cw,0);
          motorGo(2,cw,0);motorGo(3,cw,0);
          thrus_ka.writeMicroseconds(1500);
          thrus_ki.writeMicroseconds(1500);
      }
      //atur PWM Motor 0-255 ---> "m1250"
      else if(inputString1.substring(0,2)=="m1"){
        int kec =inputString1.substring(2).toInt();
        motorGo(0,cw,kec);
      }
      else if(inputString1.substring(0,2)=="m2"){
        int kec =inputString1.substring(2).toInt();
        motorGo(1,cw,kec);
      }
      else if(inputString1.substring(0,2)=="m3"){
        int kec =inputString1.substring(2).toInt();
        motorGo(2,cw,kec);
      }
      else if(inputString1.substring(0,2)=="m4"){
        int kec =inputString1.substring(2).toInt();
        motorGo(3,cw,kec);
      }
      //atur PWM Motor 1100-1900 ---> "ka1400"
      else if(inputString1.substring(0,2)=="ka"){
        int kec =inputString1.substring(2).toInt();
        thrus_ka.writeMicroseconds(kec);
      }
      else if(inputString1.substring(0,2)=="ki"){
        int kec =inputString1.substring(2).toInt();
        thrus_ki.writeMicroseconds(kec);
      }
      inputString1="";
     }
   }
}
