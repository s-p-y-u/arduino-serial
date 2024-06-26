#include <Arduino.h>
#include "parser.h"
/*
Обозначение на плате	Обозначение в прошивке	Возможности пина
TX1	                  1	                      Цифровой ввод/вывод, Serial TX
RX0	                  0	                      Цифровой ввод/вывод, Serial RX
RST		                                        Пин перезагрузки
GND		                                        Земля или V-
D2	                  2	                      Цифровой ввод/вывод
D3	                  3	                      Цифровой ввод/вывод, ШИМ
D4	                  4	                      Цифровой ввод/вывод
D5	                  5	                      Цифровой ввод/вывод, ШИМ
D6	                  6	                      Цифровой ввод/вывод, ШИМ
D7	                  7	                      Цифровой ввод/вывод
D8	                  8	                      Цифровой ввод/вывод
D9	                  9	                      Цифровой ввод/вывод, ШИМ
D10	                  10	                    Цифровой ввод/вывод, ШИМ, SPI SS
D11	                  11	                    Цифровой ввод/вывод, ШИМ, SPI MOSI
D12	                  12	                    Цифровой ввод/вывод, SPI MISO
D13	                  13	                    Цифровой ввод/вывод, LED, SPI SCK
3.3V		                                       3.3 В
REF		                                        Пин опорного напряжения
A0	A0 или 14	Аналоговый пин с 8-ми битным АЦП
A1	A1 или 15	Аналоговый пин с 8-ми битным АЦП
A2	A2 или 16	Аналоговый пин с 8-ми битным АЦП
A3	A3 или 17	Аналоговый пин с 8-ми битным АЦП
A4	A4 или 18	Аналоговый пин с 8-ми битным АЦП, I2C SDA
A5	A5 или 19	Аналоговый пин с 8-ми битным АЦП, I2C SCL
A6	A6	Аналоговый пин с 8-ми битным АЦП
A7	A7	Аналоговый пин с 8-ми битным АЦП
5V		5 В или V+
RES		Пин перезагрузки
GND		Земля или V-
VIN		Пин питания
*/

#define led__red_d3 3
#define led__green_d5 5
#define led__blue_d6 6
#define led__white_d11 11

#define led__d2 2
#define led__d4 4
#define led__d7 7
#define led__d8 8
#define led__d9 9
#define led__d10 10
#define led__d12 12

int red = 0;
int green = 0;
int blue = 0;
int white = 0;
int brightness = 0;
// int read__d = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);
// Пины D9 и D10 - 31.4 кГц
  TCCR1A = 0b00000001;  // 8bit
  TCCR1B = 0b00000001;  // x1 phase correct

  pinMode(led__red_d3, OUTPUT);
  pinMode(led__green_d5, OUTPUT);
  pinMode(led__blue_d6, OUTPUT);
  pinMode(led__white_d11, OUTPUT);
  pinMode(led__d2, OUTPUT);
  pinMode(led__d4, OUTPUT);
  pinMode(led__d7, OUTPUT);
  pinMode(led__d8, OUTPUT);
  pinMode(led__d9, OUTPUT);
  pinMode(led__d10, OUTPUT);
  pinMode(led__d12, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    char str[30];
    char amount = Serial.readBytesUntil(';', str, 30);
    str[amount] = NULL;

    Parser data(str, ',');
    int ints[24];
    data.parseInts(ints);
    // int am = data.split();
    // Serial.print(ints[0]);
    switch (ints[0]) {
      case 0:
        brightness = ints[5];
        red = int((ints[1]*brightness)/100);
        green = int((ints[2]*brightness)/100);
        blue = int((ints[3]*brightness)/100);
        white = int((ints[4]*brightness)/100);
        analogWrite(led__red_d3,red);
        analogWrite(led__green_d5,green);
        analogWrite(led__blue_d6,blue);
        analogWrite(led__white_d11,white);
        // Serial.print(red);
        // Serial.print(brightness);
        break;
      case 2:
        digitalWrite(led__d2, ints[1]);
        Serial.print("led__d2");
        break;
      case 4:
        digitalWrite(led__d4, ints[1]);
        Serial.print("led__d4");
        break;
      case 8:
        digitalWrite(led__d8, ints[1]);
        Serial.print("led__d8");
        break;
      case 9:
        digitalWrite(led__d9, ints[1]);
        Serial.print("led__d9");
        break;
      case 10:
        analogWrite(led__d10, ints[1]);
        // Serial.print(analogRead(led__d10)/4);
        break;
      case 12:
        digitalWrite(led__d12, ints[1]);
        Serial.print("led__d12");
        break;
      default:
        Serial.print("default");
        break;  
    }
  }
}
