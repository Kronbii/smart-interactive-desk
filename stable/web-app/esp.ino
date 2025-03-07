#include <HardwareSerial.h>

//TODO: make tilting and up-down work together
// Commuinication pins between ESP32 and laptop
#define RXD2 16
#define TXD2 17

// Stepper motor pins
#define STEP1 22
#define DIR1 23
#define STEP2 19
#define DIR2 18

// Stepper motor configuration
#define STEP_DELAY 500  // Microseconds delay between steps
#define STEPS_PER_CYCLE 200  // Adjust steps as needed

#define RPWM 14   // Right PWM
#define LPWM 12    // Left PWM

// Initialize serial communication between esp and laptop
HardwareSerial laptop(2);

// Direction and movement flags
bool vertical_move = false;
bool tilt_move = false;
bool vertical_dir = false;
bool tilt_dir = false;


void setup() {
    pinMode(STEP1, OUTPUT);
    pinMode(DIR1, OUTPUT);
    pinMode(STEP2, OUTPUT);
    pinMode(DIR2, OUTPUT);
    
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);

    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);

    stop_table();
}

void loop() {

    if (Serial.available() > 0) {
        String ramy = Serial.readStringUntil('\n');  // Read full command
        ramy.trim();  // Remove whitespace and newline

        if (ramy == "u") {         // Move forward
            vertical_move = true;
            vertical_dir = true;
            tilt_move = false;
            tilt_dir = false;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "d") {  // Move backward
            vertical_move = true;
            vertical_dir = false;
            tilt_move = false;
            tilt_dir = false;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "s") {  // Stop
            vertical_move = false;
            tilt_move = false;
            vertical_dir = false;
            tilt_dir = false;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "tu") {
            vertical_move = false;
            vertical_dir = false;
            tilt_move = true;
            tilt_dir = true;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "td"){
            vertical_move = false;
            vertical_dir = false;
            tilt_move = true;
            tilt_dir = false;
            laptop.println(ramy); // Debugging output
        } else {
            vertical_move = false;
            vertical_dir = false;
            tilt_move = false;
            tilt_dir = false;
            laptop.println("Unknown command: " + ramy); // Debugging output
        }
    }

if (vertical_move && vertical_dir) {
    move_table_up();
}
else if (vertical_move && !vertical_dir) {
        move_table_down();
    }
else if (tilt_move && tilt_dir) {
    tilt_table_cw();
}
else if (tilt_move && !tilt_dir) {
    tilt_table_ccw();
}
else {
    stop_table();
}
}

void move_table_up() {
    digitalWrite(RPWM, HIGH);
    digitalWrite(LPWM, LOW);
}

void move_table_down() {
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, HIGH);
}

void stop_table() {
    digitalWrite(RPWM, LOW);
    digitalWrite(LPWM, LOW);
}

void tilt_table_cw() {
    digitalWrite(DIR1, HIGH);
    digitalWrite(DIR2, HIGH);
    digitalWrite(STEP1, HIGH);
    digitalWrite(STEP2, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(STEP1, LOW);
    digitalWrite(STEP2, LOW);
    delayMicroseconds(STEP_DELAY);
}

void tilt_table_ccw() {
    digitalWrite(DIR1, LOW);
    digitalWrite(DIR2, LOW);
    digitalWrite(STEP1, HIGH);
    digitalWrite(STEP2, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(STEP1, LOW);
    digitalWrite(STEP2, LOW);
    delayMicroseconds(STEP_DELAY);
}