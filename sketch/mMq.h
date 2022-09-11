#pragma once

#define SEALEVELPRESSURE_HPA (1013.25)
#define ADC_BIT             10
#define ADC_VALUE_MAX       pow(2, ADC_BIT)
#define RP 5 
#define VOLTAGE   5.0

class mMQ {
private:
    uint8_t _pin;
public:
    mMQ(uint8_t pin);
    float readRatio() const;
    float readRs() const;
    float calcResistance(int sensorADC) const;
    float readScaled(float a, float b) const;
    unsigned long readLPG();
    unsigned long readMethane();
    unsigned long readSmoke();
    unsigned long readHydrogen();
};

mMQ::mMQ(uint8_t pin) {
  _pin = pin;
}

float mMQ::readRs() const {
  float rs = 0;
  for (int i = 0; i < 3; i++) {
    rs += calcResistance(analogRead(_pin));
    delay(300);
  }
  rs = rs / 3;
  return rs;
}

float mMQ::calcResistance(int sensorADC) const {
  float sensorVoltage = sensorADC * (VOLTAGE / ADC_VALUE_MAX);
  float sensorResistance = (VOLTAGE - sensorVoltage) / sensorVoltage * RP;
  return sensorResistance;
}

float mMQ::readScaled(float a, float b) const {
  float ratio = readRatio();
  return exp((log(ratio) - b) / a);
}

float mMQ::readRatio() const {
  return readRs() / 9.83;
}

unsigned long mMQ::readLPG() {
  return readScaled(-0.45, 2.95);
}

unsigned long mMQ::readMethane() {
  return readScaled(-0.38, 3.21);
}

unsigned long mMQ::readSmoke() {
  return readScaled(-0.42, 3.54);
}
