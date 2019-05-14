#include <SoftwareSerial.h>

SoftwareSerial ezo_board(10,11);

void setup() {
  Serial.begin(9600);
  Serial.println("Begining Programming");
  pinMode(LED_BUILTIN,OUTPUT);
  pinMode(A0,OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
  digitalWrite(A0,LOW);
  Serial.println("Entering Standby");
}

void loop() {
  //indicate standby with LED pattern
  digitalWrite(LED_BUILTIN,HIGH);
  delay(25);
  digitalWrite(LED_BUILTIN,LOW);
  delay(25);
  digitalWrite(LED_BUILTIN,HIGH);
  delay(25);
  digitalWrite(LED_BUILTIN,LOW);
  delay(250);
}
