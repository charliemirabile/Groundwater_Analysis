#include <SPI.h>
#include <RH_RF95.h>
#include <Wire.h>                 //for I2C

#define frequency 1000            //take readings every x ms
#define max_sensor_name_length 10
#define max_reading_length 10

const char* sensors[2] = {"100", "101"};
char* message[max_sensor_name_length + max_reading_length + 2];
char  computerdata[20];           //we make a 20 byte character array to hold incoming data from a pc/mac/other.
byte  received_from_computer = 0; //we need to know how many characters have been received.
byte  serial_event = 0;           //a flag to signal when data has been received from the pc/mac/other.
byte  response_code = 0;           //used to hold the I2C response code.
char  RTD_data[20];               //we make a 20 byte character array to hold incoming data from the RTD circuit.
byte  in_char = 0;                //used as a 1 byte buffer to store in bound bytes from the RTD Circuit.
byte  i = 0;                      //counter used for RTD_data array.
int   time_ = 600;                //used to change the delay needed depending on the command sent to the EZO Class RTD Circuit.
float tmp_float;                  //float var used to hold the float value of the RTD.

//for feather32u4
#define RFM95_CS  8
#define RFM95_RST 4
#define RFM95_INT 7

/* for ESP w/featherwing */
#if defined(ESP8266)
#define RFM95_CS  2    // "E"
#define RFM95_RST 16   // "D"
#define RFM95_INT 15   // "B"

/* ESP32 feather w/wing */
#elif defined(ESP32)
#define RFM95_RST     27   // "A"
#define RFM95_CS      33   // "B"
#define RFM95_INT     12   //  next to A

/* nRF52832 feather w/wing */
#elif defined(NRF52)
#define RFM95_RST     7   // "A"
#define RFM95_CS      11   // "B"
#define RFM95_INT     31   // "C"

/* Teensy 3.x w/wing */
#elif defined(TEENSYDUINO)
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

void get_reading( ) {

  for ( int j = 0 ; j < sizeof( sensors ) / sizeof( char* ) ; j++ ) {
    
    //call the circuit by its ID number.
    Wire.beginTransmission( 100+j );

    //transmit the command that was sent through the serial port.
    Wire.write(computerdata);

    //end the I2C data transmission.
    Wire.endTransmission();

    //if  the command that has been sent is the sleep command, we do nothing.
    //Issuing a sleep command and then requesting data will wake the RTD circuit.

    //if the command that has been sent is NOT the sleep command
    if ( strcmp( computerdata, "sleep" ) != 0 ) {

      //wait the correct amount of time for the circuit to complete its instruction
      delay( frequency );

      // and request data by calling the circuit and requesting 20 bytes (this may be more than we need)
      Wire.requestFrom( 100+j, 20, 1 );

      // RESPONSE CODE

      //the first byte is the response code, we read this separately.
      response_code = Wire.read();

      switch ( response_code ) {

        //decimal 1.
        case 1:

          //the command was successful.
          Serial.println("Success");

          break;

        //decimal 2.
        case 2:

          //the command has failed.
          Serial.println("Failed");

          break;

        //decimal 254.
        case 254:

          //the command has not yet been finished calculating.
          Serial.println("Pending");

          break;

        //decimal 255.
        case 255:

          //means there is no further data to send.
          Serial.println("No Data");

          break;

      }

      // RECEIVING DATA FROM SENSOR

      //are there bytes to receive?
      while ( Wire.available() ) {

        //receive a byte.
        in_char = Wire.read();

        //load this byte into our array.
        RTD_data[i] = in_char;

        //incur the counter for the array element.
        i += 1;

        //if we see that we have been sent a null command.
        if ( in_char == 0 ) {

          //reset the counter i to 0.
          i = 0;

          //end the I2C data transmission.
          Wire.endTransmission();

          //exit the while loop.
          break;

        }

      }

      //print the data.
      Serial.print("Reading from Address ");
      Serial.print(100+j);
      Serial.print(": ");
      Serial.print(RTD_data);
      Serial.print( "\n" );

      // SENDING DATA TO BASE STATION OVER RADIO

      Serial.println( "Sending message over radio.\n" );
      
      rf95.send( (uint8_t *) sensors[j], 50 );
      rf95.send( (uint8_t *) ":", 2 );
      rf95.send( (uint8_t *) RTD_data, 50 );
      delay( 10 );
      rf95.waitPacketSent();

      serial_event = false;               //reset the serial event flag.

    }
  }
}

//Uncomment this section if you want to take the RTD value and convert it into floating point number.
//RTD_float=atof(RTD_data);

void setup() {
  //Setup Radio Reset Pin
  pinMode(RFM95_RST, OUTPUT);

  //Set the active low reset pin high
  digitalWrite(RFM95_RST, HIGH);

  //Manual reset
  delay(10);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  //Start serial communication with computer
  Serial.begin(9600);

  while (!Serial) {

    //Wait for serial connection to be established
    delay(1);

  }

  //Start I2C communication with temperature sensor
  Wire.begin();

  if (!rf95.init()) {

    //Error - no radio init
    Serial.println("LoRa radio init failed");

    //hang forever
    while (1);

  }

  Serial.println("LoRa radio init success");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {

    //Error - unable to set frequency
    Serial.println("setFrequency failed");

    //hang forever
    while (1);

  }

  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ); Serial.print("\n");

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);

  sensorResponse.reserve(50);
  sensorCommand.reserve(50);

}

void loop() {

  if ( Serial.available() ) {

    received_from_computer = Serial.readBytesUntil( 13, computerdata, 20 );
    computerdata[received_from_computer] = 0;
    serial_event = true;

  }

  // CONTINUOUS READINGS

  computerdata[0] = 'r';

  while ( 1 ) {

    get_reading( );

  }

}
