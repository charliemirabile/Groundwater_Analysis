#ifndef EZO_H

#define EZO_H

#define SIZE_EZO_BUFFER 50

char ezo_reading_buffer[SIZE_EZO_BUFFER] = {'\0'};

void send_sleep_command(int sensor_address){
  Wire.beginTransmission(sensor_address);
  Wire.write("Sleep");//tell it to go to sleep
  Wire.endTransmission();
}

int get_temperature_reading(int sensor_address, char* result_buffer)
{
  Wire.beginTransmission(sensor_address);
  Wire.write("R");//ask for a reading
  Wire.endTransmission();
  delay(600);
  Wire.requestFrom(sensor_address,SIZE_EZO_BUFFER,1);//request more than enough bytes
  if(Wire.read() != 1)
  {
    //Serial.print("error reading from device at address: ");Serial.println(sensor_address);
    Wire.endTransmission();//clean up - stop the current read transmission
    send_sleep_command(sensor_address);//put the device to sleep
    return -1;//return -1 to indicate that the error occured
  }
  else
  {
    int location = 0;
    while(Wire.available() && location < SIZE_EZO_BUFFER)//while there are still bytes to read, and we havent exceeded max length
    {
      if((result_buffer[location++] = Wire.read()) == '\0') //the assignment operation we check here against does the work, and evaluates as the char written so if it is a null terminator:
      {

        break;//we got a null terminator so exit the loop
      }
    }
    Wire.endTransmission();//clean up - stop the current read transmission
    send_sleep_command(sensor_address);//put the device to sleep
    return location;//return the number of characters that we wrote to the buffer
  }
}
int get_temperature_calibrated_sensor_reading(int sensor_address, char* temperature_reading_buffer, int length_of_temp, char* result_buffer)
{
  Wire.beginTransmission(sensor_address);
  Wire.write('R');Wire.write('T');Wire.write(',');Wire.write(temperature_reading_buffer,length_of_temp);//send the callibrate and take readind command
  Wire.endTransmission();
  delay(300);
  Wire.requestFrom(sensor_address,SIZE_EZO_BUFFER,1);//request more than enough bytes
  if(Wire.read() != 1)
  {
    Serial.print("error reading from device at address: ");Serial.println(sensor_address);
    Wire.endTransmission();//clean up - stop the current read transmission
    send_sleep_command(sensor_address);//put the device to sleep
    return -1;//return -1 to indicate that the error occured
  }
  else
  {
    int location = 0;
    while(Wire.available() && location < SIZE_EZO_BUFFER)//while there are still bytes to read, and we havent exceeded max length
    {
      if((result_buffer[location++] = Wire.read()) == '\0') //the assignment operation we check here against does the work, and evaluates as the char written so if it is a null terminator:
      {

        break;//we got a null terminator so exit the loop
      }
    }
    Wire.endTransmission();//clean up - stop the current read transmission
    send_sleep_command(sensor_address);//put the device to sleep
    return location;//return the number of characters that we wrote to the buffer
  }
}

#endif