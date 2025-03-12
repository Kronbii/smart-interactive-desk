#include <HardwareSerial.h>

// Commuinication pins between ESP32 and laptop
#define RXD2 16
#define TXD2 17

// Stepper motor pins
#define M1IN1 19
#define M1IN2 18
#define M2IN1 5
#define M2IN2 4

#define RPWM 23   // Right PWM
#define LPWM 22    // Left PWM

// Initialize serial communication between esp and laptop
HardwareSerial laptop(2);

// Direction and movement flags
bool move_up_flag = false;
bool move_down_flag = false;
bool tilt_up_flag = false;
bool tilt_down_flag = false;
bool stop_motion_flag = true;

void setup() {
    pinMode(M1IN1, OUTPUT);
    pinMode(M1IN2, OUTPUT);
    pinMode(M2IN1, OUTPUT);
    pinMode(M2IN2, OUTPUT);
    
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

        if (ramy == "u") {
            // Update Flags
            move_up_flag = true;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;

            // Debug
            laptop.println(ramy); // Debugging output
        } else if (ramy == "d") {  // Move backward
            // Update Flags
            move_up_flag = false;
            move_down_flag = true;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;

            // Debug
            laptop.println(ramy); // Debugging output
        } else if (ramy == "s") {  // Stop
            // Update Flags
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;

            // Debug
            laptop.println(ramy); // Debugging output
        } else if (ramy == "r") {
            // Update Flags
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = true;
            tilt_down_flag = false;
            stop_motion_flag = false;

            // Debug
            laptop.println(ramy); // Debugging output
        } else if (ramy == "l"){
            // Update Flags
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = true;
            stop_motion_flag = false;

            // Debug
            laptop.println(ramy); // Debugging output
        } else {
            // Update Flags
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;

            // Debug
            laptop.println("Unknown command: " + ramy); // Debugging output
        }
    }

    if (move_up_flag && !stop_motion_flag) {
        move_table_up();
    }
    else if (move_down_flag && !stop_motion_flag) {
        move_table_down();
    }
    else if (tilt_up_flag && !stop_motion_flag) {
        tilt_table_up();
    }
    else if (tilt_down_flag && !stop_motion_flag) {
        tilt_table_down();
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
    digitalWrite(M1IN1, LOW);
    digitalWrite(M1IN2, LOW);
    digitalWrite(M2IN1, LOW);
    digitalWrite(M2IN2, LOW);
}

void tilt_table_up() {
    digitalWrite(M1IN1, HIGH);
    digitalWrite(M1IN2, LOW);
    digitalWrite(M2IN1, HIGH);
    digitalWrite(M2IN2, LOW);
}

void tilt_table_down() {
    digitalWrite(M1IN1, LOW);
    digitalWrite(M1IN2, HIGH);
    digitalWrite(M2IN1, LOW);
    digitalWrite(M2IN2, HIGH);
}