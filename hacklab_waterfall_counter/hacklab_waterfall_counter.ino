//Pin connected to ST_CP of 74HC595
int latchPin = 8;
//Pin connected to SH_CP of 74HC595
int clockPin = 12;
////Pin connected to DS of 74HC595
int dataPin = 11;

unsigned long counter = 0;
int t = 1;

void setup() {
  //set pins to output because they are addressed in the main loop
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  digitalWrite(clockPin, LOW);
}

void loop() {
  
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, counter);
  shiftOut(dataPin, clockPin, LSBFIRST, (counter>>8));
  shiftOut(dataPin, clockPin, LSBFIRST, (counter>>16));
  shiftOut(dataPin, clockPin, LSBFIRST, (counter>>24));
  delay(1);
  digitalWrite(latchPin, HIGH);
  delay(1);
  
  //delay(t);
  
  counter++;

}

