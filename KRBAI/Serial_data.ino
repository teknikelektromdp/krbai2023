void tampil(){
  Serial.print("roll: ");               // Display roll data
  Serial.print(roll);
  
  Serial.print("    pitch: ");          // Display pitch data
  Serial.print(pitch);
  
//  Serial.print("    angle full: ");     // Display 16 bit angle with decimal place
//  Serial.print(angle16 / 10, DEC);
//  Serial.print(".");
//  Serial.print(angle16 % 10, DEC);

//  Serial.print("    angle 8: ");        // Display 8bit angle
//  Serial.println(angle8, DEC);
  Serial.print("    Yaw (angle): ");
  Serial.println(yaw);

  delay(100);
  

}

