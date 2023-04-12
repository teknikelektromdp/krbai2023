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

