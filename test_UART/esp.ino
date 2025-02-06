#include <HardwareSerial.h>

#define RXD2 16  // GPIO16 as RX
#define TXD2 17  // GPIO17 as TX
#define LED_BUILTIN 2

HardwareSerial laptop(2); // Use Serial2

void setup() {
  raspi.begin(115200);  // Initialize raspi Monitor for debugging
  laptop.begin(115200, SERIAL_8N1, RXD2, TXD2); // Initialize Serial2 with defined pins
  laptop.println("ESP32 Ready to communicate with Raspberry Pi");
}

void loop() {
  if (laptop.available() > 0) {
    String input = laptop.readString();
    input.trim(); // Trim the input
    if (input == "1") {
      // Send signal to Raspberry Pi to start processing
      raspi.print('1');
      laptop.println("Signal sent to Raspberry Pi to start processing");
    }
  }

  if (raspi.available() > 0) {
    String dataFromPi = raspi.readStringUntil('\n');
    if (dataFromPi.length() > 0) {
      laptop.println("Data received from Raspberry Pi: " + dataFromPi);
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }

  delay(1000); // Adjust delay as needed
  digitalWrite(LED_BUILTIN, LOW);
}

https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
