#include <SPI.h>
#include <RH_RF95.h>

#include <SoftwareSerial.h>

#define TEMP_RX 11
#define TEMP_TX 10

SoftwareSerial tempSensorSerial(TEMP_RX,TEMP_TX);

 //for feather32u4 
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7

#if defined(ESP8266)
  /* for ESP w/featherwing */ 
  #define RFM95_CS  2    // "E"
  #define RFM95_RST 16   // "D"
  #define RFM95_INT 15   // "B"

#elif defined(ESP32)  
  /* ESP32 feather w/wing */
  #define RFM95_RST     27   // "A"
  #define RFM95_CS      33   // "B"
  #define RFM95_INT     12   //  next to A

#elif defined(NRF52)  
  /* nRF52832 feather w/wing */
  #define RFM95_RST     7   // "A"
  #define RFM95_CS      11   // "B"
  #define RFM95_INT     31   // "C"
  
#elif defined(TEENSYDUINO)
  /* Teensy 3.x w/wing */
  #define RFM95_RST     9   // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     4    // "C"
#endif


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

String sensorResponse = "";
String sensorCommand = "";

void setup() 
{
  pinMode(RFM95_RST, OUTPUT);//Setup Radio Reset Pin
  digitalWrite(RFM95_RST, HIGH);//Set the active low reset pin high
  //Manual reset
  delay(10);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  
  Serial.begin(9600);//Start serial communication with computer
  while (!Serial) {
    delay(1);//Wait for serial connection to be established
  }
  tempSensorSerial.begin(9600);//Start serial communication with temperature sensor
  while(!tempSensorSerial){
    delay(1);//Wait for serial connection to be established
  }

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

  sensorResponse.reserve(50);
  sensorCommand.reserve(50);
}

void loop()
{
  
  if(Serial.available()){//If we have a serial message from the computer:
    sensorCommand = Serial.readStringUntil(13);//read it into the command buffer
    tempSensorSerial.print(sensorCommand);tempSensorSerial.print('\r');//send the command to the sensor
  }
  if(tempSensorSerial.available()){//If we have a serial message from the sensor
    sensorResponse = tempSensorSerial.readStringUntil(13);//read it into the reponse buffer
    Serial.print(sensorResponse);Serial.print('\r');//Send it to the computer
    char message[50] = "";
    int i=0;
    while(i<sensorResponse.length()){
      message[i] = sensorResponse.charAt(i);
      i++;
    }
    message[49]='\0';
    Serial.println("sending message over radio");
    rf95.send((uint8_t *)message,50);
    delay(10);
    rf95.waitPacketSent();
  }
  /*
  delay(1000); // Wait 1 second between transmits, could also 'sleep' here!
  Serial.println("Transmitting..."); // Send a message to rf95_server
  
  char radiopacket[20] = "Hello World #      ";
  itoa(packetnum++, radiopacket+13, 10);
  Serial.print("Sending "); Serial.println(radiopacket);
  radiopacket[19] = 0;
  
  Serial.println("Sending...");
  delay(10);
  rf95.send((uint8_t *)radiopacket, 20);

  Serial.println("Waiting for packet to complete..."); 
  delay(10);
  rf95.waitPacketSent();
  // Now wait for a reply
  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
  uint8_t len = sizeof(buf);

  Serial.println("Waiting for reply...");
  if (rf95.waitAvailableTimeout(1000))
  { 
    // Should be a reply message for us now   
    if (rf95.recv(buf, &len))
   {
      Serial.print("Got reply: ");
      Serial.println((char*)buf);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);    
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
  else
  {
    Serial.println("No reply, is there a listener around?");
  }
  */
  
}
