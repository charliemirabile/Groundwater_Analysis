#include <SoftwareSerial.h>

#define TO_EZO_RX 11
#define TO_EZO_TX 10
#define EZO_GROUND 9

void double_blink(void)
{
  digitalWrite(LED_BUILTIN,HIGH);
  delay(25);
  digitalWrite(LED_BUILTIN,LOW);
  delay(200);
  digitalWrite(LED_BUILTIN,HIGH);
  delay(25);
  digitalWrite(LED_BUILTIN,LOW);
}

void ezo_disconnect_ground(void)
{
  pinMode(EZO_GROUND,INPUT);
}

void ezo_connect_ground(void)
{
  pinMode(EZO_GROUND,OUTPUT);
  digitalWrite(EZO_GROUND,LOW);
}

void setup() {
  //setup LED pin and ensure LED is off
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);

  //ensure the ground pin is disconnected
  ezo_disconnect_ground();

  //disconnect RX and TX pins by making them inputs which are hi-z by default
  pinMode(TO_EZO_RX,INPUT);
  pinMode(TO_EZO_TX,INPUT);

  //wait a bit before blinking so that the user can tell them apart from the reset lights
  delay(500);
  //blink to tell user to hold down button
  double_blink();
  delay(300);
  double_blink();

  //try to begin Serial
  Serial.begin(9600);
  //wait until serial is ready bc user has opened window so they have time to press button
  while(!Serial)delay(10);

  Serial.println("Begining Programming");

  ezo_connect_ground();

  delay(5000);

  ezo_disconnect_ground();

  //tell user button should be released
  double_blink();
  delay(300);
  double_blink();

  //give time to realease button
  delay(2000);

  ezo_connect_ground();

  SoftwareSerial ezo_board(TO_EZO_TX,TO_EZO_RX);
  ezo_board.begin(9600);

  while(!ezo_board.isListening())delay(10);
  
  Serial.println("Board is ready, Please enter I2C Address");
  String addr_string = Serial.readString();
  int addr = addr_string.toInt();//safe - returns zero if unable to convert which is invalid
  while(addr<8 || addr> 119)
  {
    Serial.println("Please enter address, must be an integer between 8 and 119");
    addr_string = Serial.readString();
    addr = addr_string.toInt();
  }

  String msg = String("I2C,");
  msg.concat(addr_string);
  ezo_board.println(msg);
  Serial.println("Entering Standby");
}

void loop() {
  //indicate standby with LED pattern
  double_blink();
  delay(700);
}
