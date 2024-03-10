#include "parser.h"
#define ard__led 13

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  pinMode(ard__led, OUTPUT);

}

void loop() {
  if (Serial.available()) {
    char str[30];
    char amount = Serial.readBytesUntil(';', str, 30);
    str[amount] = NULL;

    Parser data(str, ',');
    int ints[5];
    int am = data.parseInts(ints);
    // int am = data.split();
    switch (ints[0]) {
      case 0:
        digitalWrite(ard__led, ints[1]);
        break;
      case 1:
        digitalWrite(ard__led, ints[1]);
        break;
      case 2:
        break;
    }
  }
}