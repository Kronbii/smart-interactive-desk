#include <HardwareSerial.h>

// Stepper motor pins
#define M1IN1 5
#define M1IN2 4
#define M2IN1 2
#define M2IN2 3

#define RPWM 7   // Right PWM
#define LPWM 6   // Left PWM

bool freeze_table_flag = false;

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

    pinMode(10, INPUT_PULLUP); // Set pin 10 as an input with internal pull-up resistor

    Serial1.begin(9600);    // Main serial communication
    Serial.begin(9600);    // Main serial communication

    attachInterrupt(digitalPinToInterrupt(10), freeze_table, FALLING);  // Trigger on pin 10 falling edge (button press)

    stop_table();
}

void loop() {
      if (freeze_table_flag) {
        stop_table();  // If the table is frozen, stop all movements
        return;
    }

    if (Serial1.available() > 0) {
        String ramy = Serial1.readStringUntil('\n');  // Read full command
        ramy.trim();  // Remove whitespace and newline

        if (ramy == "u") {
            move_up_flag = true;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            Serial.println(ramy);
        } else if (ramy == "d") {
            move_up_flag = false;
            move_down_flag = true;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            Serial.println(ramy);
        } else if (ramy == "s") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
            Serial.println(ramy);
        } else if (ramy == "tu") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = true;
            tilt_down_flag = false;
            stop_motion_flag = false;
            Serial.println(ramy);
        } else if (ramy == "td") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = true;
            stop_motion_flag = false;
            Serial.println(ramy);
        } else {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
            Serial.println("Unknown command: " + ramy);
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

void freeze_table() {
    if (freeze_table_flag) {
        Serial.println("Table is frozen!");  // Print message when frozen
    } else {
        Serial.println("Table is unfrozen!");  // Print message when unfrozen
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
