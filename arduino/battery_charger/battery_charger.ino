void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial)delay(10);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(analogRead(A9));
  delay(500);
}
