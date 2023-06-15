void serialEvent1() {
   while (Serial1.available()) {
     char inChar = (char)Serial1.read();
     inputString2 += inChar;
     if (inChar == '\n') {
       if(inputString2.substring(0,2)=="st"){
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
       else if(inputString2.substring(0,1)=="x"){
          int pixelx = inputString2.substring(1).toInt();
          pixel_x = pixelx;
          Serial.print("Pixel_X ="); Serial.println(pixel_x);
        }
        else if(inputString2.substring(0,1)=="y"){
          int pixely = inputString2.substring(1).toInt();
          pixel_y = pixely;
          Serial.print("Pixel_Y ="); Serial.println(pixel_y);
        }
       inputString2="";
     }
   }
}
