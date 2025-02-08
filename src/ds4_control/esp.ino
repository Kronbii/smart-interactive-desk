#include <HardwareSerial.h>

// Define pins
#define RPWM 15   // Right PWM
#define LPWM 2    // Left PWM
#define RXD2 16
#define TXD2 17
#define LED_BUILTIN 2

HardwareSerial laptop(2);

bool dir = false;  // Direction flag
bool move = false; // Movement flag

void setup() {
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);
    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);

    // Ensure motor is stopped at startup
    stopMotor();
}

void loop() {
    if (Serial.available() > 0) {
        String ramy = Serial.readStringUntil('\n');  // Read full command
        ramy.trim();  // Remove whitespace and newline

        if (ramy == "u") {         // Move forward
            move = true;
            dir = true;
        } else if (ramy == "d") {  // Move backward
            move = true;
            dir = false;
        } else if (ramy == "s") {  // Stop motor
            move = false;
        } else {  
            laptop.println("Unknown command: " + ramy); // Debugging output
        }
    }

    // Control motor movement
    if (move && dir) {
        moveForward();
    } else if (move && !dir) {
        moveBackward();
    } else {
        stopMotor();
    }
}

// Function to move forward
void moveForward() {
    digitalWrite(RPWM, HIGH);
    digitalWrite(LPWM, LOW);
}

// Function to move backward
void moveBackward() {
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, HIGH);
}

// Function to stop the motor
void stopMotor() {
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, LOW);
}
