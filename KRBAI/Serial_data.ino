void tampil(){
  Serial.print("roll: ");               // Display roll data
  Serial.print(roll);
  Serial.print("    pitch: ");          // Display pitch data
  Serial.print(pitch);
  Serial.print("    Yaw (angle): ");
  Serial.println(yaw);
  delay(100);
}

