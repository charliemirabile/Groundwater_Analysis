// INCLUDES

#include <Wire.h>                     //for I2C communication
#include <RHTcpProtocol.h>
#include <RH_NRF51.h>
#include <RH_RF24.h>
#include <RHDatagram.h>
#include <RHGenericDriver.h>
#include <RHReliableDatagram.h>
#include <RH_RF95.h>
#include <RadioHead.h>
#include <RHCRC.h>
#include <RH_CC110.h>
#include <RH_MRF89.h>
#include <RH_RF69.h>
#include <RH_NRF24.h>
#include <RH_TCP.h>
#include <RHRouter.h>
#include <RHSoftwareSPI.h>
#include <RH_Serial.h>
#include <RHGenericSPI.h>
#include <radio_config_Si4460.h>
#include <RHNRFSPIDriver.h>
#include <RH_NRF905.h>
#include <RHHardwareSPI.h>
#include <RH_ASK.h>
#include <RHSPIDriver.h>
#include <RH_RF22.h>
#include <RHMesh.h>

// MACROS

#define min_address 8                 //min possible EZO address
#define max_address 119               //min possible EZO address
#define number_of_EZO_sensors 10      //how many EZO sensors do we expect to read from, at most?
#define frequency 1000                //how often will we read in data from the sensors, in ms?
#define max_reading_length 10         //how long will the data read in from the sensor be at most?
#define RFM95_CS  8                   //for feather32u4
#define RFM95_RST 4                   //for feather32u4
#define RFM95_INT 7                   //for feather32u4
#define RF95_FREQ 915.0               //RX frequency for our feather32u4

// VARIABLE DECLARATIONS

int     addresses
        [number_of_EZO_sensors] =
        {100, 101, 50, 51, 0};           //an int array containing the addresses of the EZO sensors, potentially 8-119
char    message                       //a string which we will transmit to the base station's Feather device via radio;
        [4 + max_reading_length];     //3 chars for the address, 1 char for a colon, and max_reading_length chars for the sensor's read-in data
char    computerdata[20];             //a 20-byte char array containing the incoming data from the computer
byte    received_from_computer = 0;   //how many characters have been received from the computer?
byte    serial_event = 0;             //a flag to signal when data has been received from the pc/mac/other.
byte    response_code = 0;            //used to hold the I2C response code.
char    RTD_data[20];                 //a 20-byte char array containing the incoming data from the RTD circuit
byte    in_char = 0;                  //a 1-byte buffer storing inbound bytes from the RTD Circuit
byte    i = 0;                        //a counter used for RTD_data array
int     time_ = 600;                  //used to change the delay needed depending on the command sent to the EZO Class RTD Circuit
float   tmp_float;                    //float var used to hold the float value of the RTD
String  sensorResponse = "";
String  sensorCommand = "";

// FUNCTION DECLARATIONS

void  get_reading( );
void  send_sleep_command( int sensor_address );
int   get_temperature_reading( int sensor_address, char* result_buffer );
int   get_temperature_calibrated_sensor_reading(int sensor_address, char* temperature_reading_buffer, int length_of_temp, char* result_buffer);

// SINGLETON INSTANCE OF THE RADIO DRIVER

RH_RF95 rf95(RFM95_CS, RFM95_INT);

// SETUP FUNCTION

void setup() {
  
  //Start (potential) serial communication with computer
  Serial.begin(9600);

//  while (!Serial) {
//
//    //Wait for serial connection to be established
//    delay(1);
//
//  }

  //Start I2C communication
  Wire.begin();

  //Setup Radio
  pinMode(RFM95_RST, OUTPUT);//configure reset pin

  //Set the active low reset pin high
  digitalWrite(RFM95_RST, HIGH);

  //Manual reset
  delay(10);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  if (!rf95.init()) {

    //Error - no radio init
    Serial.println("LoRa radio init failed");

    //hang forever
    while (1);

  }

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {

    //Error - unable to set frequency
    Serial.println("setFrequency failed");

    //hang forever
    while (1);

  }

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);

  sensorResponse.reserve(50);
  sensorCommand.reserve(50);

}

void loop() {

//  if ( Serial.available() ) {
//
//    received_from_computer = Serial.readBytesUntil( 13, computerdata, 20 );
//    computerdata[received_from_computer] = 0;
//    serial_event = true;
//
//  }

  // CONTINUOUS READINGS

  computerdata[0] = 'r';

  while ( 1 ) {

    get_reading( );

  }

}

void get_reading( ) {

  for ( int j = 0 ; j < sizeof( addresses ) / sizeof( int ) ; j++ ) {

    if ( addresses[j] >= min_address && addresses[j] <= max_address ) {
    
    //call the circuit by its ID number.
    Wire.beginTransmission( addresses[j] ) ;

    //transmit the command that was sent through the serial port.
    Wire.write( computerdata ) ;

    //end the I2C data transmission.
    Wire.endTransmission();

    //if  the command that has been sent is the sleep command, we do nothing.
    //Issuing a sleep command and then requesting data will wake the RTD circuit.

    //if the command that has been sent is NOT the sleep command
    if ( strcmp( computerdata, "sleep" ) != 0 ) {

      //wait the correct amount of time for the circuit to complete its instruction
      delay( frequency );

      // and request data by calling the circuit and requesting 20 bytes (this may be more than we need)
      Wire.requestFrom( addresses[j], 20, 1 ) ;

      // RESPONSE CODE

      //the first byte is the response code, we read this separately.
      response_code = Wire.read();

      switch ( response_code ) {

        //decimal 1.
        case 1:

          //the command was successful.
          Serial.print("Command entered:           "); Serial.print(computerdata); Serial.print("\n");
          Serial.println("Command status:            SUCESSFUL.");

          break;

        //decimal 2.
        case 2:

          //the command has failed.
          Serial.print("Command entered:           "); Serial.print(computerdata); Serial.print("\n");
          Serial.println("Command status:            FAILED.");

          break;

        //decimal 254.
        case 254:

          //the command has not yet been finished calculating.
          Serial.print("Command entered:           "); Serial.print(computerdata); Serial.print("\n");
          Serial.println("Command status:            PENDING");

          break;

        //decimal 255.
        case 255:

          //means there is no further data to send.
          Serial.print("Command entered:           "); Serial.print(computerdata); Serial.print("\n");
          Serial.println("Command status:            NO DATA");

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
      Serial.print("Reading from Address:      ");
      Serial.print(addresses[j]);
      Serial.print( "\n" );
      
      Serial.print("Read in:                   ");
      Serial.print(RTD_data);
      Serial.print( "\n" );

      // PREPARE THE MESSAGE TO SEND TO BASE STATION OVER RADIO
      
      int n = sprintf( message, "%d : %s", addresses, RTD_data );

      // SENDING DATA TO BASE STATION OVER RADIO

      Serial.print("Will send over radio:      " );
      Serial.print(message);
      Serial.print("\n");

      rf95.send( (uint8_t *) message, 4 + max_reading_length );
      
      Serial.println("\nMessage sent!\n\n\n" );
 
      delay( 10 );
      rf95.waitPacketSent();

      serial_event = false;               //reset the serial event flag.

    }
    
  }

  }
  
}

void send_sleep_command( int sensor_address ) {
  
  Wire.beginTransmission( sensor_address ) ;

  //tell it to go to sleep
  Wire.write( "Sleep" ) ;
  
  Wire.endTransmission( ) ;

}

int get_temperature_reading( int sensor_address, char* result_buffer ) {
  
  Wire.beginTransmission( sensor_address ) ;

  //ask for a reading
  Wire.write( "R" );
  
  Wire.endTransmission( ) ;
  
  delay( 600 ) ;

  //request more than enough bytes
  Wire.requestFrom( sensor_address, max_reading_length, 1 ) ;
  
  if ( Wire.read( ) != 1 ) {
    
    Serial.print( "error reading from device at address: " ) ;
    Serial.println( sensor_address ) ;

    //clean up - stop the current read transmission
    Wire.endTransmission( ) ;

    //put the device to sleep
    send_sleep_command( sensor_address ) ;

    //return -1 to indicate that the error occured
    return -1;
  
  } else {
    
    int location = 0 ;

    //while there are still bytes to read, and we havent exceeded max length
    while ( Wire.available() && location < max_reading_length ) {

      //the assignment operation we check here against does the work
      // and evaluates as the char written so if it is a null terminator:
      if((result_buffer[location++] = Wire.read()) == '\0') {

        //we got a null terminator so exit the loop
        break;
        
      }
      
    }

    //clean up - stop the current read transmission
    Wire.endTransmission();

    //put the device to sleep
    send_sleep_command(sensor_address);

    //return the number of characters that we wrote to the buffer
    return location;
    
  }
  
}

int get_temperature_calibrated_sensor_reading(int sensor_address, char* temperature_reading_buffer, int length_of_temp, char* result_buffer) {
  
  Wire.beginTransmission(sensor_address);
  
  Wire.write('R');Wire.write('T');Wire.write(',');Wire.write(temperature_reading_buffer,length_of_temp);//send the callibrate and take readind command
  
  Wire.endTransmission();
  
  delay(300);
  
  Wire.requestFrom(sensor_address,max_reading_length,1);//request more than enough bytes
  
  if(Wire.read() != 1) {
    
    Serial.print("error reading from device at address: ");Serial.println(sensor_address);

    //clean up - stop the current read transmission
    Wire.endTransmission();

    //put the device to sleep
    send_sleep_command(sensor_address);

    //return -1 to indicate that the error occured
    return -1;
    
  } else {
    
    int location = 0;

    //while there are still bytes to read, and we havent exceeded max length
    while(Wire.available() && location < max_reading_length) {

      //the assignment operation we check here against does the work, and evaluates as the char written so
      //if it is a null terminator:
      if((result_buffer[location++] = Wire.read()) == '\0') {

        //we got a null terminator so exit the loop
        break;
        
      }
      
    }

    //clean up - stop the current read transmission
    Wire.endTransmission();
    
    //put the device to sleep
    send_sleep_command(sensor_address);

    //return the number of characters that we wrote to the buffer
    return location;
    
  }
  
}
  

