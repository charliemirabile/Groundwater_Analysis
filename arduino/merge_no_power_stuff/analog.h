#ifndef ANALOG_H

#define ANALOG_H

#define SIZE_ANALOG_BUFFER 20

#define BAT_PIN A9
#define BAT_STRING "7"

char analog_reading_buffer[SIZE_ANALOG_BUFFER];

void format_analog_reading(int analog_pin_number, char* result_buffer)
{
  //Note: BAT_STRING = "7" and "7"":%d" is treated the same as "7:%d" by the compiler
  sprintf(result_buffer, BAT_STRING":%d", analog_pin_number, analogRead(analog_pin_number));
}

void format_battery_reading(char* result_buffer)
{
  sprintf(result_buffer, "%d:%d", analog_pin_number, analogRead(analog_pin_number));
}

#endif
