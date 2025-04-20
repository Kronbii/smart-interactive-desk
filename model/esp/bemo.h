#ifndef BEMO_H
#define BEMO_H

#include <Arduino.h>
#include <HardwareSerial.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include "Adafruit_VL53L0X.h"
#include <HCSR04.h>

// === TOF SENSOR PINS === //
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31
#define SHT_LOX1 9
#define SHT_LOX2 8

// === MANUAL CONTROL === //
#define man_up_pin A8
#define man_down_pin A9
#define man_tilt_up_pin A10
#define man_tilt_down_pin A11

// === TILTING MOTORS PINS === //
#define M1IN1 5
#define M1IN2 4
#define M2IN1 3
#define M2IN2 2

// === LIFTING MOTORS PINS === //
#define RPWM 7
#define LPWM 6

bool manual_active = false; // Tracks if manual control was recently active

Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();
VL53L0X_RangingMeasurementData_t measure1;
VL53L0X_RangingMeasurementData_t measure2;

// === Kalman Filter Class === //
class KalmanFilter {
  public:
    KalmanFilter(float q, float r, float p, float initialValue) {
      Q = q;
      R = r;
      P = p;
      X = initialValue;
    }

    float update(float measurement) {
      P = P + Q;
      K = P / (P + R);
      X = X + K * (measurement - X);
      P = (1 - K) * P;
      return X;
    }

  private:
    float Q, R, P, K, X;
};

// === Serial Communication Class === //
class SerialComm {
  public:
    void begin(long baudrate) {
      Serial.begin(baudrate);
    }

    void readCommand(String &command) {
      if (Serial.available() > 0) {
        command = Serial.readStringUntil('\n');
        command.trim();
      }
    }

    void writeStatus(float height, float tilt) {
      Serial.print("POS:");
      Serial.print(height);
      Serial.print(",");
      Serial.println(tilt);
    }
};

// === Motion Control Class === //
class MotionControl {
  public:
    void init() {
      pinMode(M1IN1, OUTPUT); pinMode(M1IN2, OUTPUT);
      pinMode(M2IN1, OUTPUT); pinMode(M2IN2, OUTPUT);
      pinMode(RPWM, OUTPUT);  pinMode(LPWM, OUTPUT);
      this->stop();
    }

    void moveUp()    { digitalWrite(RPWM, HIGH); digitalWrite(LPWM, LOW); }
    void moveDown()  { digitalWrite(RPWM, LOW);  digitalWrite(LPWM, HIGH); }
    void stop() {
      digitalWrite(RPWM, LOW); digitalWrite(LPWM, LOW);
      digitalWrite(M1IN1, LOW); digitalWrite(M1IN2, LOW);
      digitalWrite(M2IN1, LOW); digitalWrite(M2IN2, LOW);
    }
    void tiltUp()    { digitalWrite(M1IN1, HIGH); digitalWrite(M1IN2, LOW); digitalWrite(M2IN1, HIGH); digitalWrite(M2IN2, LOW); }
    void tiltDown()  { digitalWrite(M1IN1, LOW);  digitalWrite(M1IN2, HIGH); digitalWrite(M2IN1, LOW);  digitalWrite(M2IN2, HIGH); }
};

// === Table Status Class === //
class TableStatus {
  public:
    byte triggerPin = 12;
    byte echoPin = 22;
    double height = 0;
    double tilt = 0;

    void init() {
      this->height = 0;
      this->tilt = 0;
    }
    double getHeight(){
      return this->height;
    }

    double getTilt(){
      return this->tilt;
    }

    void setHeight(double height){
      this->height = height;
    }

    void setTilt(double tilt){
      this->tilt = tilt;
    }
};

void read_dual_sensors(int &sensor1Reading, int &sensor2Reading) {
  lox1.rangingTest(&measure1, false);
  lox2.rangingTest(&measure2, false);
  sensor1Reading = (measure1.RangeStatus != 4) ? measure1.RangeMilliMeter : -1;
  sensor2Reading = (measure2.RangeStatus != 4) ? measure2.RangeMilliMeter : -1;
}

void man_control(String &command){
  bool man_up = digitalRead(man_up_pin);
  bool man_down = digitalRead(man_down_pin);
  bool man_tilt_up = digitalRead(man_tilt_up_pin);
  bool man_tilt_down = digitalRead(man_tilt_down_pin);

  if (man_up == LOW) {
    command = "u";
  } else if (man_down == LOW) {
    command = "d";
  } else if (man_tilt_up == LOW) {
    command = "tu";
  } else if (man_tilt_down == LOW) {
    command = "td";
  } else {
    command = "s";
  }
  Serial.println(command);
  delay(100);
}

#endif // BEMO_H
