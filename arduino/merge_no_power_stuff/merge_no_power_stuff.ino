#include "I2C.h"
#include "radio.h"


void setup() {
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

  setup_i2c(address_array);
  Serial.println(address_array[0]);
 //Steps:
 //init wire, radio, maybe serial?
 //scan i2c addresses
 //maybe send some sort of diagnostic report over serial if it is connected?
}

void loop() {
  //Check battery; send message if low
  //Scan all valid i2c addresses and transmit readings or error stuff?
  //Scan the 6 analogue pins
  //Go to sleep
}
