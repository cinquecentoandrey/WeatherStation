#include <Adafruit_BME280.h>
#include <Wire.h> 
#include <Adafruit_Sensor.h>
#include "mMq.h"

#define TEMP 0
#define HUM 1
#define PRES 2
#define MET 3
#define CO2 4

mMQ mq2(A0);
Adafruit_BME280 bme;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(soundPin, OUTPUT);
  Serial.setTimeout(5);
  if (!bme.begin(0x76)) {
      Serial.println("Could not find a valid BME280 sensor, check wiring!");
      while (1);
    }
}

void loop() {
  static uint32_t tmr = 0;
  if (millis() - tmr > 100) {
    tmr = millis();
    Serial.print(TEMP);
    Serial.print(',');
    Serial.println(bme.readTemperature());
    
    Serial.print(HUM);
    Serial.print(',');
    Serial.println(bme.readHumidity());

    Serial.print(PRES);
    Serial.print(',');
    Serial.println(bme.readPressure() / 1.3 / 100);
    
    Serial.print(MET);
    Serial.print(',');
    Serial.println(mq2.readMethane());
    
    Serial.print(CO2);
    Serial.print(',');
    Serial.println(mq2.readSmoke());
  }
}
