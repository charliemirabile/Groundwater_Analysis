#ifndef EZO_H

#define EZO_H

#define SIZE_EZO_RESPONSE 40

char _ezo_response[SIZE_EZO_RESPONSE] = {'\0'};

#define SIZE_EZO_BUFFER 50

char ezo_reading_buffer[SIZE_EZO_BUFFER] = {'\0'};

// preconditions:
//  - sensor_address is the address of an EZO board or the analog pin number where the sensor needs to be put to sleep
// postcondition:
//  - the sleep command is sent to device at sensor_address
//  - nothing is returned

void send_sleep_command(int sensor_address){
  Wire.beginTransmission(sensor_address);
  Wire.write("Sleep");//tell it to go to sleep
  Wire.endTransmission();
}

// preconditions:
//  - sensor_address is the address of an EZO board or the analog pin number where the sensor is taking a temperature reading
//  - result_buffer is a null terminated string where sensor_address followed by ':' followed by the temperature reading will be stored
// postcondition:
//  - EZO board reading is taken at sensor_address, the reading is stored in result_buffer, and the sensor at sensor_address is put to sleep.
//  - the number of characters that we wrote to the buffer is returned

int get_sensor_reading(int sensor_address, char* result_buffer)
{
  Wire.beginTransmission(sensor_address);
  Wire.write("R");//ask for a reading
  Wire.endTransmission();
  delay(2000);
  Wire.requestFrom(sensor_address,SIZE_EZO_RESPONSE,1);//request more than enough bytes
  if(Wire.read() != 1)
  {
    //Serial.print("error reading from device at address: ");Serial.println(sensor_address);
    send_sleep_command(sensor_address);//put the device to sleep
    return -1;//return -1 to indicate that the error occured
  }
  else
  {
    int location = 0;
    while(Wire.available() && location < SIZE_EZO_RESPONSE)//while there are still bytes to read, and we havent exceeded max length
    {
      if((_ezo_response[location++] = Wire.read()) == '\0') //the assignment operation we check here against does the work, and evaluates as the char written so if it is a null terminator:
      {
        break;//we got a null terminator so exit the loop
      }
    }
    sprintf(result_buffer, "%d:%s", sensor_address, _ezo_response);
    send_sleep_command(sensor_address);//put the device to sleep
    return location;//return the number of characters that we wrote to the buffer
  }
}

// preconditions:
//  - sensor_address
//  - temperature_reading_buffer 
//  - length_of_temp
//  - result_buffer
// postconditions:
//  - the command 'RT' is sent to the sensor
//  - the number of characters that we wrote to the buffer is returned

int get_temperature_calibrated_sensor_reading(int sensor_address, char* temperature_reading_buffer, int length_of_temp, char* result_buffer)
{
  Wire.beginTransmission(sensor_address);
  Wire.write('T');Wire.write(',');Wire.write(temperature_reading_buffer,length_of_temp);//send the callibrate and take reading command
  Wire.endTransmission();
  delay(2000);
  Wire.beginTransmission(sensor_address);
  Wire.write('R');
  Wire.endTransmission();
  delay(1000);
  Wire.requestFrom(sensor_address,SIZE_EZO_BUFFER,1);//request more than enough bytes
  if(Wire.read() != 1)
  {
    //Serial.print("error reading from device at address: ");Serial.println(sensor_address);
    send_sleep_command(sensor_address);//put the device to sleep
    return -1;//return -1 to indicate that the error occured
  }
  else
  {
    int location = 0;
    while(Wire.available() && location < SIZE_EZO_RESPONSE)//while there are still bytes to read, and we havent exceeded max length
    {
      if((_ezo_response[location++] = Wire.read()) == '\0') //the assignment operation we check here against does the work, and evaluates as the char written so if it is a null terminator:
      {
        break;//we got a null terminator so exit the loop
      }
    }
    sprintf(result_buffer, "%d:%s", sensor_address, _ezo_response);
    send_sleep_command(sensor_address);//put the device to sleep
    return location;//return the number of characters that we wrote to the buffer
  }
}

#endif
