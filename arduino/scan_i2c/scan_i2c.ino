#include <Wire.h>

#define MAXADDRESSES 15

int i2cAddresses[MAXADDRESSES]={0};//this initializes all of the values to zero

void setup() {
  Serial.begin(9600);
  while(!Serial)delay(5);
  Wire.begin();
  Serial.println("Begin.");
}

void loop() {
    Serial.println("Scanning...");
  scan_i2c_bus(i2cAddresses,MAXADDRESSES);
    Serial.println("Found:");
  for(int i=0;i<MAXADDRESSES;i++)
  {
    if(i2cAddresses[i]!=0)Serial.println(i2cAddresses[i]);
  }

  delay(2000);
}

void scan_i2c_bus(int* pAddressArray, int max_addresses)
{
  int address,status_code;
  int next_index_to_fill=0;
  for(address=8;address<120&&next_index_to_fill<max_addresses;address++)//iterate over addresses 8-119 and ensure we dont fill past end of array
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
