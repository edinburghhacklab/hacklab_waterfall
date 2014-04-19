//Pin connected to ST_CP of 74HC595
int latchPin = 8;
//Pin connected to SH_CP of 74HC595
int clockPin = 12;
////Pin connected to DS of 74HC595
int dataPin = 11;

int ledPin = 13;

unsigned long counter = 0;
int t = 1;
byte inputString[256];

byte read_serial_byte() {
  while (Serial.available() == 0) {
  }
  return (byte)Serial.read();
}

void setup() {
  //set pins to output because they are addressed in the main loop
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  digitalWrite(clockPin, LOW);
  
  pinMode(ledPin, OUTPUT);
  
    // initialize serial
  Serial.begin(115200);
  
  // and wait for it to become available
  while (!Serial) ;

}

void loop() {
  byte msg_length;
  int i;
  
  msg_length = read_serial_byte();
  
  if (msg_length > 0) {
    for (i=0; i<msg_length; i++) {
      inputString[i] = read_serial_byte();
    }

    if (msg_length==8) {
      digitalWrite(ledPin, HIGH);
      digitalWrite(latchPin, LOW);
      for (i=0; i<8; i++) {
        shiftOut(dataPin, clockPin, MSBFIRST, 255-(inputString[i]));
      }
      digitalWrite(latchPin, HIGH);
      digitalWrite(ledPin, LOW);
    }
  }

}

