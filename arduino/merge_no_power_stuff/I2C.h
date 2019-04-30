#ifndef I2C_H

#define I2C_H


#include <Wire.h>

#define MIN_VALID_ADDRESS 8
#define MAX_VALID_ADDRESS 119

#define MAX_DEVICES 10

int address_array[MAX_DEVICES]={0};
//Precondition: pAddressArray is a pointer to allocated memory
//Postcondition: iterates over all possible addresses and sees which ones give a response.
//Stores the ones that give a response in the array pointed to by pAddressArray.
void scan_i2c_bus(int* pAddressArray, int max_addresses)
{
  int address,status_code;
  int next_index_to_fill=0;
  for(address=MIN_VALID_ADDRESS;address<=MAX_VALID_ADDRESS && next_index_to_fill<max_addresses; address++)
  //iterate over addresses 8-119 and ensure we dont fill past end of array
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

//Precondition: pArray is a pointer to allocated memory
//Postcondition: Begins i2c transmission and calls scan_i2c_bus to find all devices on the bus
bool setup_i2c(int* pArray)
{
  Wire.begin();
  scan_i2c_bus(pArray,MAX_DEVICES);
  return true;
}

#endif
