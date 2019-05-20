#ifndef RADIO_H

#define RADIO_H

#include <RH_RF95.h> //Radio Library


//Specific pin number definitions for the feather
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7

//Specify the frequency
#define RF95_FREQ 915.0


#define FEATHER_ID "1337"

#define SIZE_RADIO_BUFFER 50

char radio_message_buffer[SIZE_RADIO_BUFFER] = {'\0'};

//Instanciate the singleton instance of rf95 to do radio comms.
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// preconditions:
//  - no arguments
// postconditions:
//  - if radio is successfully set up, return true

bool setup_radio()
{
  pinMode(RFM95_RST, OUTPUT);
  //Set the active low reset pin high
  digitalWrite(RFM95_RST, HIGH);

  //Manual reset
  delay(10);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  
  if (!rf95.init())return false;
  
  if (!rf95.setFrequency(RF95_FREQ))return false;

  rf95.setTxPower(23, false);
  return true;
}

// preconditions:
//  - message_buffer is a string that contains the message to be sent via radio
// postconditions:
//  - message_buffer is set and sent via radio

void send_radio_message(char* message_buffer)
{
  sprintf(radio_message_buffer, FEATHER_ID ":%s", message_buffer);
  rf95.send((uint8_t*)radio_message_buffer, SIZE_RADIO_BUFFER);
  rf95.waitPacketSent();
}


#endif
