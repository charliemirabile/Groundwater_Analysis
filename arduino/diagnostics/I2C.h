#ifndef I2C_H

#define I2C_H
#define max_reading_length 10


#include <Wire.h>

#define MIN_VALID_ADDRESS 8
#define MAX_VALID_ADDRESS 119

#define MAX_DEVICES 10

int address_array[MAX_DEVICES]={0};

void scan_i2c_bus(int* pAddressArray, int max_addresses)
{
  int address,status_code;
  int next_index_to_fill=0;
  for(address=MIN_VALID_ADDRESS;address<=MAX_VALID_ADDRESS && next_index_to_fill<max_addresses; address++)//iterate over addresses 8-119 and ensure we dont fill past end of array
  {
    Wire.beginTransmission(address);
    status_code = Wire.endTransmission(true);
    if(status_code==0)
    {
      pAddressArray[next_index_to_fill]=address;
      next_index_to_fill += 1;
    }
  }
}


bool setup_i2c(int* pArray)
{
  Wire.begin();
  scan_i2c_bus(pArray,MAX_DEVICES);
  return true;
}

int get_device_information(int sensor_address, char* result_buffer)
{
  Wire.beginTransmission(sensor_address);
  Wire.write("I");//ask for a reading
  Wire.endTransmission();
  delay(600);
  Wire.requestFrom(sensor_address,max_reading_length,1);//request more than enough bytes
  if(Wire.read() != 1)
  {
    //Serial.print("error reading from device at address: ");Serial.println(sensor_address);
    Wire.endTransmission();//clean up - stop the current read transmission
    //send_sleep_command(sensor_address);//put the device to sleep
    return -1;//return -1 to indicate that the error occured
  }
  else
  {
    int location = 0;
    while(Wire.available() && location < max_reading_length)//while there are still bytes to read, and we havent exceeded max length
    {
      if((result_buffer[location++] = Wire.read()) == '\0') //the assignment operation we check here against does the work, and evaluates as the char written so if it is a null terminator:
      {

        break;//we got a null terminator so exit the loop
      }
    }
    Wire.endTransmission();//clean up - stop the current read transmission
    //send_sleep_command(sensor_address);//put the device to sleep
    return location;//return the number of characters that we wrote to the buffer
  }
}

#endif
