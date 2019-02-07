#include <stdio.h>
#include <RH_RF95.h>
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7
#define RF95_FREQ 915.0
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  if (!rf95.init()) {
    //Error - no radio init
    Serial.println("LoRa radio init failed");
    while (1);//hang forever
  }
  Serial.println("LoRa radio init success");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    //Error - unable to set frequency
    Serial.println("setFrequency failed");
    while (1);//hang forever
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);
  
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

void loop() {
  // reads pins A0 through A5:
  int i;
  char buffer[16];
  for(i = 0; i < 6; i++)
  {
    sprintf(buffer, "%d:%d", i, (analogRead(A0 + i)));
    Serial.println(buffer);
    rf95.send((uint8_t*)buffer, 16);
  }
  
  //Serial.print("\n\n\n\n");
  rf95.send((uint8_t*)"\n\n\n", 4);
  delay(1000);
}
