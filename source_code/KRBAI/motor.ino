void motorGo(int motor, int direct, int pwm)
{
  if (motor <= 4)
  {
    if (direct == 0)
    {
      digitalWrite(inApin[motor], HIGH);
      digitalWrite(inBpin[motor], LOW);
    }
    else if (direct == 1)
    {
      digitalWrite(inApin[motor], LOW);
      digitalWrite(inBpin[motor], HIGH);
    }
  }
  analogWrite(pwmpin[motor], pwm);
}

void forward()
{
  motorGo(0,cw,75);
  motorGo(1,ccw,100);
  motorGo(2,cw,75);
  motorGo(3,cw,100);
}
void back()
{
  motorGo(0,ccw,75);
  motorGo(1,cw,75);
  motorGo(2,ccw,75);
  motorGo(3,ccw,75);
}
void shift_left()
{
  motorGo(0,ccw,75);
  motorGo(1,ccw,75);
  motorGo(2,cw,75);
  motorGo(3,ccw,75);
}
void shift_right()
{
  motorGo(0,cw,75);
  motorGo(1,cw,75);
  motorGo(2,ccw,75);
  motorGo(3,cw,75);
}
void right_rotate()
{
  motorGo(0,cw,75);
  motorGo(1,cw,75);
  motorGo(2,cw,75);
  motorGo(3,ccw,75);
}
void rr_PID(int kec)
{
  motorGo(0,cw,kec);
  motorGo(1,cw,kec);
  motorGo(2,cw,kec);
  motorGo(3,ccw,kec);
}
void left_rotate()
{
  motorGo(0,ccw,75);
  motorGo(1,ccw,75);
  motorGo(2,ccw,75);
  motorGo(3,cw,75);
}
void lr_PID(int kec)
{
  motorGo(0,ccw,kec);
  motorGo(1,ccw,kec);
  motorGo(2,ccw,kec);
  motorGo(3,cw,kec);
}
void berhenti()
{
  motorGo(0,cw,0);
  motorGo(1,cw,0);
  motorGo(2,cw,0);
  motorGo(3,cw,0);
}
void SOS()
{
  mode = false; head = false;
  berhenti();
  thrus_ka.writeMicroseconds(1500);
  thrus_ki.writeMicroseconds(1500);
  for(int i=0;i<10;i++){
    digitalWrite(46, HIGH);
    delay(500);
    digitalWrite(46, LOW);
    delay(500);
  }
  digitalWrite(46, HIGH);
  
}
