void tampil(){
//  Serial.print("roll: ");          Serial.print(roll);
//  Serial.print(", pitch: ");       Serial.print(pitch);
  Serial.print(", Yaw(angle): ");  Serial.println(yaw);

//  Serial.print("SP_depth(cm): ");    Serial.print(set_level);
//  Serial.print(", set_point: ");        Serial.print(de_Setpoint);
//  Serial.print(", Pressure: ");   Serial.print(avg);
//  Serial.print(", water_lvl: ");  Serial.println(water_level);
//  Serial.println(de_Output);
  delay(100);
}

void serialEvent() {
   while (Serial.available()) {
     char inChar = (char)Serial.read();
     inputString1 += inChar;
     if (inChar == '\n') {
      if(inputString1.substring(0,2)=="st"){
//          motorGo(0,cw,0);motorGo(1,cw,0);
//          motorGo(2,cw,0);motorGo(3,cw,0);
          thrus_ka.writeMicroseconds(1500);
          thrus_ki.writeMicroseconds(1500);
          thrus_pi.writeMicroseconds(1500);
          thrus_1.writeMicroseconds(1500);
          thrus_2.writeMicroseconds(1500);
          thrus_3.writeMicroseconds(1500);
          thrus_4.writeMicroseconds(1500);
          Serial.println("OK STOP");
      }
      else if(inputString1.substring(0,2)=="au"){
          //program auto misi 1
          misi = !misi;
      }
      else if(inputString1.substring(0,2)=="so"){
          SOS();
      }
      else if(inputString1.substring(0,2)=="pi"){
          mode = !mode;
          Serial.print("Status PID Depth: ");Serial.println(mode);
      }
      else if(inputString1.substring(0,2)=="he"){
          head = !head;
          Serial.print("Status PID Head: ");Serial.println(head);
      }
      else if(inputString1.substring(0,2)=="ob"){
          objek = !objek;
          Serial.println("Objek Detection");
      }
      /*
      else if(inputString1.substring(0,1)=="x"){
        int pixelx = inputString1.substring(1).toInt();
        pixel_x = pixelx;
        Serial.print("Pixel_X ="); Serial.println(pixel_x);
      }
      else if(inputString1.substring(0,1)=="y"){
        int pixely = inputString1.substring(1).toInt();
        pixel_y = pixely;
        Serial.print("Pixel_Y ="); Serial.println(pixel_y);
      }
      */
      else if(inputString1.substring(0,1)=="s"){
        int nilai =inputString1.substring(1).toInt();
        EEPROM.write(1,nilai);
        set_level = nilai;
        Serial.print("Set_point"); Serial.println(nilai);
      }
      else if(inputString1.substring(0,1)=="p"){
        int pid =inputString1.substring(1).toInt();
        EEPROM.write(2,pid);
        depth_kp = EEPROM.read(2);
        Serial.print("depth_kp = "); Serial.println(depth_kp);
      }
      else if(inputString1.substring(0,1)=="i"){
        int pid =inputString1.substring(1).toInt();
        EEPROM.write(3,pid);
        depth_ki = EEPROM.read(3)*0.1;
        Serial.print("depth_ki = "); Serial.println(depth_ki);
      }
      else if(inputString1.substring(0,1)=="d"){
        int pid =inputString1.substring(1).toInt();
        EEPROM.write(4,pid);
        depth_kd = EEPROM.read(4)*0.1;
        Serial.print("depth_kd = "); Serial.println(depth_kd);
      }
      else if(inputString1.substring(0,2)=="hp"){
        int pid =inputString1.substring(2).toInt();
        EEPROM.write(5,pid);
        head_kp = EEPROM.read(5);
        Serial.print("head_kp = "); Serial.println(head_kp);
      }
      else if(inputString1.substring(0,2)=="hi"){
        int pid =inputString1.substring(2).toInt();
        EEPROM.write(6,pid);
        head_ki = EEPROM.read(6)*0.1;
        Serial.print("head_ki = "); Serial.println(head_ki);
      }
      else if(inputString1.substring(0,2)=="hd"){
        int pid =inputString1.substring(2).toInt();
        EEPROM.write(7,pid);
        head_kd = EEPROM.read(7)*0.1;
        Serial.print("head_kd = "); Serial.println(head_kd);
      }
      //atur PWM Motor 0-255 ---> "m1250"
      else if(inputString1.substring(0,2)=="m1"){
        int kec =inputString1.substring(2).toInt();
        //mundur
        motorGo(0,ccw,kec);   Serial.println("ok motor 1");
      }
      else if(inputString1.substring(0,2)=="m2"){
        int kec =inputString1.substring(2).toInt();
        //maju
        motorGo(1,ccw,kec);   Serial.println("ok motor 2");
      }
      else if(inputString1.substring(0,2)=="m3"){
        int kec =inputString1.substring(2).toInt();
        //maju
        motorGo(2,cw,kec);    Serial.println("ok motor 3");
      }
      else if(inputString1.substring(0,2)=="m4"){
        int kec =inputString1.substring(2).toInt();
        //mundur
        motorGo(3,ccw,kec);   Serial.println("ok motor 4");
      }
      //atur PWM Motor 1300-1700 ---> "ka1400"
      else if(inputString1.substring(0,2)=="ka"){
        int kec =inputString1.substring(2).toInt();
        thrus_ka.writeMicroseconds(kec);  Serial.println("ok motor Kanan");
      }
      else if(inputString1.substring(0,2)=="ki"){
        int kec =inputString1.substring(2).toInt();
        thrus_ki.writeMicroseconds(kec);  Serial.println("ok motor Kiri");
      }
      else if(inputString1.substring(0,2)=="fo"){
        forward(); Serial.println("ok Forward");
      }
      else if(inputString1.substring(0,2)=="ba"){
        back(); Serial.println("ok Backward");
      }
      else if(inputString1.substring(0,2)=="ri"){
        shift_right(); Serial.println("ok shift_right");
      }
      else if(inputString1.substring(0,2)=="le"){
        shift_left(); Serial.println("ok shift_left");
      }
      else if(inputString1.substring(0,2)=="ro"){
        right_rotate(); Serial.println("ok right_rotate");
      }
      else if(inputString1.substring(0,2)=="lo"){
        left_rotate(); Serial.println("ok left_rotate");
      }
      else if(inputString1.substring(0,2)=="la"){
        state = !state;
        digitalWrite(47, state); 
        Serial.print("Lamp ");Serial.println(state);
      }
      inputString1="";
     }
   }
}
