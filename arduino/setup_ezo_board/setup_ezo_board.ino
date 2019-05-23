#include <SoftwareSerial.h>

//PINS
#define TO_EZO_RX 11
#define TO_EZO_TX 10
#define TO_EZO_GROUND 9

/*Wiring:

Connect EZO Vcc to 3.3v on board
Connect EZO GND,TX,RX to pins from avove
Connect rightmost lower pin of EZO board to one side of normally open pushbotton
Connect other side of button to TX on EZO

*/

typedef enum {I2C,UART} State;

//FUNCTION DEFINTIONS
State get_state(void);
void wait_for_any_message(void);
void ezo_disconnect_ground(void);
void ezo_connect_ground(void);
void in_I2C(void);
int get_address(void);
void in_UART(void);

//SETUP
void setup() {
  //setup builtin LED pin
  pinMode(LED_BUILTIN,OUTPUT);
  
  //disconnect RX and TX pins by making them inputs which are hi-z by default
  pinMode(TO_EZO_RX, INPUT);
  pinMode(TO_EZO_TX, INPUT);

  ezo_connect_ground();

  //try to begin Serial
  Serial.begin(9600);
  //wait until serial is ready
  while (!Serial)delay(10);

  //Get color of LED by user input
  switch(get_state())
  {
    case UART:
    Serial.print("\n");
      in_UART();
      break;
    case I2C:
    Serial.print("\n");
      in_I2C();
      break;
  }  
  Serial.println("Entering Standby");
  //---> into loop()
}

//STANDBY - do nothing after the setup has finished
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


//FUNCTION BODIES

//Pre-condition: None
//Post-condition: returns State, based on user input (I2C or UART)
State get_state(void)
{
  String line;
  Serial.println("What color is the LED on the EZO board?");
  Serial.println("1. Solid Blue");
  Serial.println("2. Blinking/Solid Green");
  Serial.println("3. Other\n");
  Serial.print("Enter the appropriate number: ");
  while(true)
  {
    if(Serial.available())
    {
      line = Serial.readString();
      Serial.print(line);
      switch(line.toInt())
      {
        case 1://Blue
          return I2C;
        case 2://Green
          return UART;
        case 3://Wrong
          Serial.println("Error the light must be green or blue.");
          break;
        default://Wrong
          Serial.println("Error, invalid input."); 
          break;
      }
      Serial.print("Enter the appropriate number: ");
      while(Serial.available())Serial.read();
    }
    else
      delay(100);
  }
}

//----------------------------------------------------------------------

//Pre-condition: Serial buffer should be empty
//Post-condition: returns after a message has been sent, buffer will have been emptied.
void wait_for_any_message(void)
{
  while(true)
  {
    if(Serial.available())
    {
      while(Serial.available())Serial.read();
      return;
    }
    else
      delay(100);
  }
}

//----------------------------------------------------------------------

//Pre-condition: TO_EZO_GROUND pin is correctly wired on the board
//Post-condition: Ground is disconnected
void ezo_disconnect_ground(void)
{
  pinMode(TO_EZO_GROUND, INPUT);
}

//----------------------------------------------------------------------

//Pre-condition: TO_EZO_GROUND pin is correctly wired on the board
//Post-condition: Ground is connected and set to LOW
void ezo_connect_ground(void)
{
  pinMode(TO_EZO_GROUND, OUTPUT);
  digitalWrite(TO_EZO_GROUND, LOW);
}

//----------------------------------------------------------------------

//Pre-condition: ezo is powered up and in I2C mode.
//Post-condition: ezo is powered up and in UART mode.
void in_I2C(void)
{
  //Blue - therefore, the button must be pressed
  ezo_disconnect_ground();
  
   //disconnect RX and TX pins by making them inputs which are hi-z by default
  pinMode(TO_EZO_RX, INPUT);
  pinMode(TO_EZO_TX, INPUT);
  
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
  ezo_connect_ground();
  in_UART();
}

//----------------------------------------------------------------------

//Pro-condition: None
//Post-condition: returns valid I2C address that is within the range 8-119.
int get_address(void)
{
  Serial.print("Address: ");
  String addr_string;
  int addr;
  while (true)
  {
    if (Serial.available())
    {
      addr_string = Serial.readString();
      Serial.print(addr_string);
      addr = addr_string.toInt();//safe - returns zero if unable to convert which is invalid
      
      if(addr >= 8 && addr <= 119)return addr;

      Serial.println("Error invalid address, must be an integer bewteen 8 and 119");
      Serial.print("Address: ");
    }
    else
      delay(100);
  }
}

//----------------------------------------------------------------------

//Pre-condition: ezo is powered up and in UART mode.
//Post-condition: ezo is powered down after being put into I2C with the desired address.
void in_UART(void)
{
  //connect to EZO in UART MODE
  SoftwareSerial ezo_board(TO_EZO_TX, TO_EZO_RX);
  ezo_board.begin(9600);
  while (!ezo_board.isListening())delay(10);
  delay(1000);
  //disable continuous readings
  ezo_board.println("C,0");

  //Wait for a user to give a valid address
  Serial.println("Board is ready, Please enter I2C Address");
  int addr = get_address();
  Serial.println("Changing address");
  //Send message to EZO to put into I2C mode with correct address
  String msg = String("I2C,");
  String clean = String(addr);
  msg.concat(clean);
  ezo_board.println(msg);
  delay(10000);
  ezo_disconnect_ground();
}
