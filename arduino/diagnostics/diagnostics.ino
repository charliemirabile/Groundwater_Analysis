#include "I2C.h"
#include "radio.h"

char result_buffer[20] = {'\0'};

void setup() {
  
   //init wire, radio, serial
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
  for(int i=0; i<MAX_DEVICES;i++)
  {
    if(address_array[i]!=0){Serial.println(address_array[i]);
    get_device_information(address_array[i], result_buffer);
    Serial.println( result_buffer );
    }
  }

 //TODO: finish writing some sort of diagnostic report over serial if it is connected?
 
}

void loop() {
  //Check battery; send message if low
  //Scan all valid i2c addresses and transmit readings or error stuff?
  //Scan the 6 analogue pins
  //Go to sleep
}
