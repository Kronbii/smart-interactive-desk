#define STEP_PIN 15   // Step signal
#define DIR_PIN 2     // Direction control
#define RXD2 16
#define TXD2 17

#include <HardwareSerial.h>

HardwareSerial laptop(2);

bool dir = false;  // Direction flag
bool moveMotor = false; // Movement flag

void setup() {
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);

    // Ensure motor is stopped at startup
    moveMotor = false;
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // Read full command
        command.trim();  // Remove whitespace and newline

        if (command == "f") {         // Move forward
            moveMotor = true;
            dir = true;
        } else if (command == "r") {  // Move reverse
            moveMotor = true;
            dir = false;
        } else if (command == "s") {  // Stop motor
            moveMotor = false;
        } else {  
            laptop.println("Unknown command: " + command); // Debugging output
        }
    }

    // Control motor movement
    if (moveMotor) {
        moveStepper(dir);
    }
}

// Function to move stepper motor
void moveStepper(bool direction) {
    digitalWrite(DIR_PIN, direction ? HIGH : LOW);  // Set direction
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500);  // Adjust speed
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500);
}
