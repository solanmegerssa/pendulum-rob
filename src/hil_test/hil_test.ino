void setup() {
  Serial.begin(115200); // use the same baud-rate as the python side
}
void loop() {
  char inByte = ' ';
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    Serial.println(inByte); // send the data back in a new line so that it is not all one long line
  }
  delay(100); // delay for 1/10 of a second
}
