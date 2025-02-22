#include <HardwareSerial.h>

// Define pins
#define RXD2 16
#define TXD2 17

#define STEP1 3  // Step pin for Motor 1
#define DIR1 2   // Direction pin for Motor 1
#define STEP2 5  // Step pin for Motor 2
#define DIR2 4   // Direction pin for Motor 2

#define BTN_CW 6   // Button for clockwise rotation
#define BTN_CCW 7  // Button for counterclockwise rotation

#define STEP_DELAY 500  // Microseconds delay between steps

HardwareSerial laptop(2);

bool dir = false;  // Direction flag
bool move = false; // Movement flag

void setup() {
    pinMode(STEP1, OUTPUT);
    pinMode(DIR1, OUTPUT);
    pinMode(STEP2, OUTPUT);
    pinMode(DIR2, OUTPUT);

    pinMode(BTN_CW, INPUT_PULLUP);  // Internal pull-up resistor
    pinMode(BTN_CCW, INPUT_PULLUP); // Internal pull-up resistor

    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);
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
        } else {  
            laptop.println("Unknown command: " + ramy); // Debugging output
        }
    }

    if (move && dir) {
        digitalWrite(DIR1, HIGH);
        digitalWrite(DIR2, HIGH);
        rotateBothMotors();
    } else if (move && !dir) {
        digitalWrite(DIR1, LOW);
        digitalWrite(DIR2, LOW);
        rotateBothMotors();
    } else {
        
    }
}

void rotateBothMotors() {
    for (int i = 0; i < 200; i++) {  // Adjust for desired steps
        digitalWrite(STEP1, HIGH);
        digitalWrite(STEP2, HIGH);
        delayMicroseconds(STEP_DELAY);
        digitalWrite(STEP1, LOW);
        digitalWrite(STEP2, LOW);
        delayMicroseconds(STEP_DELAY);
    }
}
