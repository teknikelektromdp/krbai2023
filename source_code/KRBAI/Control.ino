void PID_Depth(float depth_kp, float depth_ki, float depth_kd, float depth)
{
  //reset_level = nilai presure permukaan
  //de_Setpoint = 1015;
  de_Setpoint = reset_level + set_level;
  de_Input =  depth;
  depth_PID.SetTunings(depth_kp,depth_ki,depth_kd);
  depth_PID.Compute();
}

void PID_Heading(float head_kp, float head_ki, float head_kd, float heading)
{
  he_Setpoint = set_head;
  he_Input =  heading;
  head_PID.SetTunings(head_kp,head_ki,head_kd);
  head_PID.Compute();
}

void PID_Roll(float roll_kp, float roll_ki, float roll_kd, float roll)
{
  ro_Setpoint = 0;
  ro_Input =  roll;
  roll_PID.SetTunings(roll_kp,roll_ki,roll_kd);
  roll_PID.Compute();
}

void PID_pitch(float pitch_kp, float pitch_ki, float pitch_kd, float pitch)
{
  pi_Setpoint = 0;
  pi_Input =  pitch;
  pitch_PID.SetTunings(pitch_kp,pitch_ki,pitch_kd);
  pitch_PID.Compute();
}
