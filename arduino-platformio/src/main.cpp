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
#define led__d2 2
#define led__white_d3 3
#define led__d4 4
#define led__d5 5
#define led__d6 6
#define led__d7 7
#define led__d8 8
#define led__red_d9 9
#define led__green_d10 10
#define led__blue_d11 11
#define led__d12 12


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  pinMode(led__d2, OUTPUT);
  pinMode(led__white_d3, OUTPUT);
  pinMode(led__d4, OUTPUT);
  pinMode(led__d5, OUTPUT);
  pinMode(led__d6, OUTPUT);
  pinMode(led__d7, OUTPUT);
  pinMode(led__d8, OUTPUT);
  pinMode(led__red_d9, OUTPUT);
  pinMode(led__green_d10, OUTPUT);
  pinMode(led__blue_d11, OUTPUT);
  pinMode(led__d12, OUTPUT);

}

void loop() {
  if (Serial.available()) {
    char str[30];
    char amount = Serial.readBytesUntil(';', str, 30);
    str[amount] = NULL;

    Parser data(str, ',');
    int ints[24];
    int am = data.parseInts(ints);
    // int am = data.split();
    switch (ints[0]) {
      case 0:
        analogWrite(led__red_d9,ints[1]);
        analogWrite(led__green_d10,ints[2]);
        analogWrite(led__blue_d11,ints[3]);
        
        analogWrite(led__white_d3,ints[4]);
        int brightness = ints[5];
        int res = 0;
        if(led__red_d9,ints[1]) res = 1;
        Serial.print(res);
        break;
      case 2:
        digitalWrite(led__d2, ints[1]);
        Serial.print("led__d2");
        break;
      // case 3:
      //   digitalWrite(led__d3, ints[1]);
      //   Serial.print("led__d3");
      //   break;
      case 4:
        digitalWrite(led__d4, ints[1]);
        Serial.print("led__d4");
        break;
      case 5:
        digitalWrite(led__d5, ints[1]);
        Serial.print("led__d5");
        break;
      case 6:
        digitalWrite(led__d6, ints[1]);
        Serial.print("led__d6");
        break;
      case 7:
        digitalWrite(led__d7, ints[1]);
        Serial.print("led__d7");
        break;
      case 8:
        digitalWrite(led__d8, ints[1]);
        Serial.print("led__d8");
        break;
      // case 9:
      //   digitalWrite(led__d9, ints[1]);
      //   Serial.print("led__d9");
      //   break;
      // case 10:
      //   digitalWrite(led__d10, ints[1]);
      //   Serial.print("led__d10");
      //   break;
      // case 11:
      //   digitalWrite(led__d11, ints[1]);
      //   Serial.print("led__d11");
      //   break;
      case 12:
        digitalWrite(led__d12, ints[1]);
        Serial.print("led__d12");
        break;  
    }
  }
  // delay(1000);
  // Serial.print("text\r\n");
}
