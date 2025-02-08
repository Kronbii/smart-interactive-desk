#include <HardwareSerial.h>
// Define pins
#define RPWM 15   // Right PWM
#define LPWM 2  // Left PWM
#define RXD2 16
#define TXD2 17
#define LED_BUILTIN 2

HardwareSerial laptop(2);

bool dir = false;
bool move = false;

void setup() {
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);
    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);

    // Ensure motor is stopped at startup
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, LOW);
}

void loop() {
  if (Serial.available() > 0) {
      String ramy = Serial.readString();
      ramy.trim();
      //laptop.println(ramy);
      if (ramy == "u") {
          move = true;
          dir = true;
          //laptop.println("UP");
      } else if (ramy == "d") {
          move = true;
          dir = false;
      } else if (ramy == "s") {
          move = false;
          dir = false;
      }
      else {
          laptop.println(ramy);
      }
  }
}

  // Move forward
  if (move && dir){
    digitalWrite(RPWM, HIGH);
    digitalWrite(LPWM, HIGH);
  }
  // Move backward
  else if (move && !dir){
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, LOW);
  }
  // Stop
  else {
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, LOW);
  }