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
  motorGo(0,ccw,220);
  motorGo(1,cw,220);
  motorGo(2,cw,220);
  motorGo(3,ccw,220);
}
void back()
{
  motorGo(0,cw,220);
  motorGo(1,ccw,220);
  motorGo(2,ccw,220);
  motorGo(3,cw,220);
}
void shift_left()
{
  motorGo(0,cw,220);
  motorGo(1,cw,220);
  motorGo(2,cw,220);
  motorGo(3,cw,220);
}
void shift_right()
{
  motorGo(0,ccw,220);
  motorGo(1,ccw,220);
  motorGo(2,ccw,220);
  motorGo(3,ccw,220);
}
void right()
{
  motorGo(0,cw,220);
  motorGo(1,cw,220);
  motorGo(2,ccw,220);
  motorGo(3,ccw,220);
}
void left()
{
  motorGo(0,ccw,220);
  motorGo(1,ccw,220);
  motorGo(2,cw,220);
  motorGo(3,cw,220);
}
void berhenti()
{
  motorGo(0,cw,0);
  motorGo(1,cw,0);
  motorGo(2,cw,0);
  motorGo(3,cw,0);
}
