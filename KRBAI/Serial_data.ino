void tampil(){
  Serial.print("roll: ");             Serial.print(roll);
  Serial.print("    pitch: ");        Serial.print(pitch);
  Serial.print("    Yaw (angle): ");  Serial.println(yaw);

  Serial.print("set_point: ");        Serial.println(de_Setpoint);
  Serial.print("Pressure: ");         Serial.println(avg);
  Serial.print("water_lvl: ");        Serial.println(water_level);
  
  delay(100);
}

