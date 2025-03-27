#include <HardwareSerial.h>

// Stepper motor pins
#define M1IN1 19
#define M1IN2 18
#define M2IN1 5
#define M2IN2 4

#define RPWM 23   // Right PWM
#define LPWM 22   // Left PWM

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

    Serial.begin(115200);    // Main serial communication
    Serial1.begin(115200);   // Use Serial1 for communication with ESP32/laptop

    stop_table();
}

void loop() {
    if (Serial.available() > 0) {
        String ramy = Serial.readStringUntil('\n');  // Read full command
        ramy.trim();  // Remove whitespace and newline

        if (ramy == "u") {
            move_up_flag = true;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            Serial1.println(ramy);
        } else if (ramy == "d") {
            move_up_flag = false;
            move_down_flag = true;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            Serial1.println(ramy);
        } else if (ramy == "s") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
            Serial1.println(ramy);
        } else if (ramy == "r") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = true;
            tilt_down_flag = false;
            stop_motion_flag = false;
            Serial1.println(ramy);
        } else if (ramy == "l") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = true;
            stop_motion_flag = false;
            Serial1.println(ramy);
        } else {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
            Serial1.println("Unknown command: " + ramy);
        }
    }

    if (move_up_flag && !stop_motion_flag) {
        move_table_up();
    } else if (move_down_flag && !stop_motion_flag) {
        move_table_down();
    } else if (tilt_up_flag && !stop_motion_flag) {
        tilt_table_up();
    } else if (tilt_down_flag && !stop_motion_flag) {
        tilt_table_down();
    } else {
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
