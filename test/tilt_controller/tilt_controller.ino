#include <HardwareSerial.h>

// Define Stepper Motor Pins
#define STEP_PIN 15   // Step signal
#define DIR_PIN 2     // Direction signal
#define RXD2 16
#define TXD2 17

HardwareSerial laptop(2);

bool dir = false;  // Direction flag
bool move = false; // Movement flag

void setup() {
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);

    // Ensure motor is stopped at startup
    stopStepper();
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // Read full command
        command.trim();  // Remove whitespace and newline

        if (command == "r") {   // Rotate clockwise
            move = true;
            dir = true;
        } else if (command == "f") {  // Rotate counterclockwise
            move = true;
            dir = false;
        } else if (command == "s") {  // Stop motor
            move = false;
        } else {  
            laptop.println("Unknown command: " + command); // Debugging output
        }
    }

    // Control stepper movement
    if (move && dir) {
        rotateClockwise();
    } else if (move && !dir) {
        rotateCounterclockwise();
    } else {
        stopStepper();
    }
}

// Function to rotate clockwise
void rotateClockwise() {
    digitalWrite(DIR_PIN, HIGH);  // Set direction
    stepMotor();
}

// Function to rotate counterclockwise
void rotateCounterclockwise() {
    digitalWrite(DIR_PIN, LOW);  // Set direction
    stepMotor();
}

// Function to step the motor
void stepMotor() {
    for (int i = 0; i < 200; i++) {  // Adjust steps per revolution as needed
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(800);  // Adjust speed
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(800);
    }
}

// Function to stop the stepper motor (optional)
void stopStepper() {
    // No specific stop function needed for stepper motors
}
