
#include <Wire.h>
//calibration value 4096
//Sending this value in two bytes is by sending 16 and 0

//FUNCTION DEFINTIONS
void reset_INA_state(int INA_address);
void calibrate_INA(int INA_address);
int get_raw_current(int INA_address);

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  Wire.begin();
  reset_INA_state(64);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:

  //Put into a safe state to stop the program
  if(Serial.available())
  {
    while(1);
  }
  
  calibrate_INA(64);
  
  Serial.println(get_raw_current(64));
 
  delay(100);
}

//FUNCTION BODIES
//----------------------------------------------------------------

//Pre-condition: AdafruitINA219 is correctly wired
//Post-condition: The INA219 has been reset to a default state 
void reset_INA_state(int INA_address)
{
  Wire.beginTransmission(64);
  //Set the target register to the configuration address
  Wire.write(0);
  //Write two bytes to reset
  Wire.write(1<<7);
  Wire.write(0);
  Wire.endTransmission();
}

//----------------------------------------------------------------

//Pre-condition: AdafruitINA219 is correctly wired
//Post-condition: The INA219 has recieved the correct bytes for calibration
void calibrate_INA(int INA_address)
{
  Wire.beginTransmission(64);
  //Set the target register to calibration address
  Wire.write(5);
  //Spliting the two bytes of 4096
  Wire.write(16);
  Wire.write(0);
  Wire.endTransmission();
}

//----------------------------------------------------------------

//Pre-condition: AdafruitINA219 is correctly wired
//Post-condition: The current reading from the INA219 is returned
int get_raw_current(int INA_address)
{
  //Set the target register to current address
  Wire.beginTransmission(64);
  Wire.write(4);
  Wire.endTransmission();
  
  delay(10);
  //Get current reading
  Wire.requestFrom(64, 2);
  delay(10);
  //Reconcatinate the two bytes essentially
  return ((Wire.read() << 8) | (Wire.read()));
}

//----------------------------------------------------------------
