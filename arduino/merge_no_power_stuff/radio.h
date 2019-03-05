#ifndef RADIO_H

#define RADIO_H

#include <RH_RF95.h> //Radio Library


//Specific pin number definitions for the feather
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7

//Specify the frequency
#define RF95_FREQ 915.0

//Instanciate the singleton instance of rf95 to do radio comms.
RH_RF95 rf95(RFM95_CS, RFM95_INT);

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



#endif
