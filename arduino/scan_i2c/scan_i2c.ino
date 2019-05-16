#include <Wire.h>

#define MAXADDRESSES 15

int i2cAddresses[MAXADDRESSES]={0};//this initializes all of the values to zero

void setup() {
  Serial.begin(9600);
  while(!Serial)delay(5);
  Wire.begin();
  Serial.println("Scanning...");
  scan_i2c_bus(i2cAddresses,MAXADDRESSES);
  Serial.println("Found:");
  for(int i=0;i<MAXADDRESSES;i++)
  {
    if(i2cAddresses[i]!=0)Serial.println(i2cAddresses[i]);
  }
  Serial.print("Enter the address of a device to make its light blink: ");
}

void loop() {
  if(Serial.available())
  {
    String line = Serial.readString();
    Serial.println(line);
    int addr = line.toInt();
    if(addr<=7||addr>=120)
    {
      Serial.println("Error invalid address, must be an integer bewteen 8 and 119");
    }
    else
    {
      Wire.beginTransmission(addr);
      Wire.write("Find");
      Wire.endTransmission();
      delay(5000);
      Wire.beginTransmission(addr);
      Wire.write(" ");
      Wire.endTransmission();
    }
    Serial.print("Enter the address of a device to make its light blink: ");
  }
  delay(100);
}

void scan_i2c_bus(int* pAddressArray, int max_addresses)
{
  int address,status_code;
  int next_index_to_fill=0;
  for(address=8;address<120&&next_index_to_fill<max_addresses;address++)//iterate over addresses 8-119 and ensure we dont fill past end of array
  {
    Wire.beginTransmission(address);
    Wire.write("derp");
    status_code = Wire.endTransmission();
    if(status_code==0)
    {
      pAddressArray[next_index_to_fill]=address;
      next_index_to_fill += 1;
    }
  }
}
