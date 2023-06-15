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
//  motorGo(0,cw,75);
//  motorGo(1,ccw,100);
//  motorGo(2,cw,75);
//  motorGo(3,cw,100);
  thrus_1.writeMicroseconds(1700);
  thrus_2.writeMicroseconds(1300);
  thrus_3.writeMicroseconds(1700);
  thrus_4.writeMicroseconds(1700);
}
void back()
{
//  motorGo(0,ccw,75);
//  motorGo(1,cw,75);
//  motorGo(2,ccw,75);
//  motorGo(3,ccw,75);
  thrus_1.writeMicroseconds(1300);
  thrus_2.writeMicroseconds(1700);
  thrus_3.writeMicroseconds(1300);
  thrus_4.writeMicroseconds(1300);
}
void shift_left()
{
//  motorGo(0,ccw,75);
//  motorGo(1,ccw,75);
//  motorGo(2,cw,75);
//  motorGo(3,ccw,75);
  thrus_1.writeMicroseconds(1300);
  thrus_2.writeMicroseconds(1300);
  thrus_3.writeMicroseconds(1700);
  thrus_4.writeMicroseconds(1300);
}
void shift_left1(int kec)
{
  thrus_1.writeMicroseconds(1500 - kec);
  thrus_2.writeMicroseconds(1500 - kec);
  thrus_3.writeMicroseconds(1500 + kec);
  thrus_4.writeMicroseconds(1500 - kec);
}
void shift_right()
{
//  motorGo(0,cw,75);
//  motorGo(1,cw,75);
//  motorGo(2,ccw,75);
//  motorGo(3,cw,75);
  thrus_1.writeMicroseconds(1700);
  thrus_2.writeMicroseconds(1700);
  thrus_3.writeMicroseconds(1300);
  thrus_4.writeMicroseconds(1700);
}
void shift_right1(int kec)
{
  thrus_1.writeMicroseconds(1500 + kec);
  thrus_2.writeMicroseconds(1500 + kec);
  thrus_3.writeMicroseconds(1500 - kec);
  thrus_4.writeMicroseconds(1500 + kec);
}
void right_rotate()
{
//  motorGo(0,cw,75);
//  motorGo(1,cw,75);
//  motorGo(2,cw,75);
//  motorGo(3,ccw,75);
  thrus_1.writeMicroseconds(1700);
  thrus_2.writeMicroseconds(1700);
  thrus_3.writeMicroseconds(1700);
  thrus_4.writeMicroseconds(1300);
}
void rr_PID(int kec)
{
//  motorGo(0,cw,kec);
//  motorGo(1,cw,kec);
//  motorGo(2,cw,kec);
//  motorGo(3,ccw,kec);
  thrus_1.writeMicroseconds(1500 + kec);
  thrus_2.writeMicroseconds(1500 + kec);
  thrus_3.writeMicroseconds(1500 + kec);
  thrus_4.writeMicroseconds(1500 - kec);
}
void left_rotate()
{
//  motorGo(0,ccw,75);
//  motorGo(1,ccw,75);
//  motorGo(2,ccw,75);
//  motorGo(3,cw,75);
  thrus_1.writeMicroseconds(1300);
  thrus_2.writeMicroseconds(1300);
  thrus_3.writeMicroseconds(1300);
  thrus_4.writeMicroseconds(1700);
}
void lr_PID(int kec)
{
//  motorGo(0,ccw,kec);
//  motorGo(1,ccw,kec);
//  motorGo(2,ccw,kec);
//  motorGo(3,cw,kec);
  thrus_1.writeMicroseconds(1500 - kec);
  thrus_2.writeMicroseconds(1500 - kec);
  thrus_3.writeMicroseconds(1500 - kec);
  thrus_4.writeMicroseconds(1500 + kec);
}
void berhenti()
{
//  motorGo(0,cw,0);
//  motorGo(1,cw,0);
//  motorGo(2,cw,0);
//  motorGo(3,cw,0);
  thrus_1.writeMicroseconds(1500);
  thrus_2.writeMicroseconds(1500);
  thrus_3.writeMicroseconds(1500);
  thrus_4.writeMicroseconds(1500);
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
