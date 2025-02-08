#include <HardwareSerial.h>

#define RXD2 16  // GPIO16 as RX
#define TXD2 17  // GPIO17 as TX
#define LED_BUILTIN 2

HardwareSerial laptop(2); // Use Serial2

void setup() {
  Serial.begin(115200);  // Initialize Serial Monitor for debugging
  laptop.begin(115200, SERIAL_8N1, RXD2, TXD2); // Initialize Serial2 with defined pins
  laptop.println("ESP32 Ready to communicate with Raspberry Pi");
}

void loop() {
  if (laptop.available() > 0) {
    String input = laptop.readString();
    input.trim(); // Trim the input
    if (input == "u") {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000); // Adjust delay as needed
      digitalWrite(LED_BUILTIN, LOW);
    }
    else if (input == "d") {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000); // Adjust delay as needed
      digitalWrite(LED_BUILTIN, LOW);
    }
    else if (input == "s") {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000); // Adjust delay as needed
      digitalWrite(LED_BUILTIN, LOW);
    }
  }

  if (Serial.available() > 0) {
    String dataFromPi = Serial.readStringUntil('\n');
    if (dataFromPi.length() > 0) {
      laptop.println(dataFromPi);
    }
  }

}
