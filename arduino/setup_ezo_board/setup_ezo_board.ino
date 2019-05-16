#include <SoftwareSerial.h>

#define TO_EZO_RX 11
#define TO_EZO_TX 10
#define EZO_GROUND 9

void wait_for_any_message(void)
{
  bool should_proceed=false;
  while(!should_proceed)
  {
    if(Serial.available())
    {
      while(Serial.available())Serial.read();
      should_proceed=true;
    }
    else delay(100);
  }
}
void ezo_disconnect_ground(void)
{
  pinMode(EZO_GROUND, INPUT);
}

void ezo_connect_ground(void)
{
  pinMode(EZO_GROUND, OUTPUT);
  digitalWrite(EZO_GROUND, LOW);
}

void setup() {
  //setup builtin LED pin
  pinMode(LED_BUILTIN,OUTPUT);

  //ensure the ground pin is disconnected so EZO is turned off
  ezo_disconnect_ground();

  //disconnect RX and TX pins by making them inputs which are hi-z by default
  pinMode(TO_EZO_RX, INPUT);
  pinMode(TO_EZO_TX, INPUT);

  //try to begin Serial
  Serial.begin(9600);
  //wait until serial is ready
  while (!Serial)delay(10);


  Serial.println("Hold down button until told to release");
  Serial.println("Send any message once holding button to proceed");
  wait_for_any_message();
  
  Serial.println("Begining Programming");

  //power up while button is pressed to reset device into UART mode
  ezo_connect_ground();
  delay(10000);
  ezo_disconnect_ground();

  Serial.println("Release Button");
  Serial.println("Send any message after releasing button to proceed");
  wait_for_any_message();


  //power up and connect to EZO in UART MOD
  ezo_connect_ground();
  SoftwareSerial ezo_board(TO_EZO_TX, TO_EZO_RX);
  ezo_board.begin(9600);
  while (!ezo_board.isListening())delay(10);


  //Wait for a user to give a valid address
  bool has_setup_addr = false;
  Serial.println("Board is ready, Please enter I2C Address");
  Serial.print("Address: ");
  String addr_string;
  int addr;
  while (!has_setup_addr)
  {
    if (Serial.available())
    {
      addr_string = Serial.readString();
      Serial.println(addr_string);
      addr = addr_string.toInt();//safe - returns zero if unable to convert which is invalid
      if (addr <= 7 || addr >= 120)
      {
        Serial.println("Error invalid address, must be an integer bewteen 8 and 119");
        Serial.print("Address: ");
      }
      else
      {
        has_setup_addr = true;
      }
    }
    else delay(100);
  }
  Serial.println("Changing address");

  //Send message to EZO to put into I2C mode with correct address
  String msg = String("I2C,");
  msg.concat(addr_string);
  ezo_board.println(msg);
  delay(10000);
  ezo_disconnect_ground();
  Serial.println("Entering Standby");
}

void loop() {
  digitalWrite(LED_BUILTIN,HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN,LOW);
  delay(200);
  digitalWrite(LED_BUILTIN,HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN,LOW);
  delay(700);
}
