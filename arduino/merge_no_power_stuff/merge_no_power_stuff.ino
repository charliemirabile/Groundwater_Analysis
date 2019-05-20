#include "I2C.h"
#include "EZO.h"
#include "radio.h"
#include "analog.h"
#include "radio.h"

void setup() {
 //Steps:
 
 //init wire, radio, maybe serial?
  Serial.begin(9600);
  while(!Serial)delay(1);

  
  bool radio_success = setup_radio();

  
  if(radio_success)
  {
    Serial.println("SUCCESS");
  }
  else
  {
    Serial.println("FAILURE");
  }
  
 //scan i2c addresses
  setup_i2c(address_array);

 //maybe send some sort of diagnostic report over serial if it is connected?
  for(int i=0; i<MAX_DEVICES;i++)
  {
    if(address_array[i]!=0)Serial.println(address_array[i]);
  }
}

void loop() {
  
  //testing code to make output more readable on RSPI
  //  send_radio_message("\n\n\n\n");

  
  //Steps:
  
  //Check battery; send message if low
  if(battery_low()){
    format_battery_reading(analog_reading_buffer);
    send_radio_message(analog_reading_buffer);
  }
  
  //Scan all valid i2c addresses and transmit readings or error stuff?

  //Needs work - doesnt callibrate readings in any way
  for(int i=0; i<MAX_DEVICES;i++)
  {
    if(address_array[i]!=0)
    {
        get_temperature_reading(address_array[i],ezo_reading_buffer);
        send_radio_message(ezo_reading_buffer);
    }
  }

//  //Scan the 6 analogue pins
  for(int i=0;i<6;i++)
  {
    format_analog_reading(A0+i, analog_reading_buffer);
    send_radio_message(analog_reading_buffer);
  }

  
  //Go to sleep
  
  delay(100);
}
