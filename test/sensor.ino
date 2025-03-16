#include <HardwareSerial.h>
#include "Adafruit_VL53L0X.h"
#include <Wire.h>

// Commuinication pins between ESP32 and laptop
#define RXD2 16
#define TXD2 17

// Stepper motor pins
#define M1IN1 19
#define M1IN2 18
#define M2IN1 5
#define M2IN2 4

#define RPWM 23   // Right PWM
#define LPWM 2    // Left PWM

// I2C Pins for VL53L0X Sensors
#define SDA_PIN 21
#define SCL_PIN 22

// Initialize serial communication between esp and laptop
HardwareSerial laptop(2);

// Direction and movement flags
bool move_up_flag = false;
bool move_down_flag = false;
bool tilt_up_flag = false;
bool tilt_down_flag = false;
bool stop_motion_flag = true;

// Create two sensor objects for distance sensing
Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();

// Calibration parameters
#define NUM_READINGS 10  // Number of readings to average
#define CALIBRATION_DELAY 100  // Delay between each reading (in milliseconds)

void setup() {
    pinMode(M1IN1, OUTPUT);
    pinMode(M1IN2, OUTPUT);
    pinMode(M2IN1, OUTPUT);
    pinMode(M2IN2, OUTPUT);
    
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);

    Serial.begin(115200);  // Start serial communication
    laptop.begin(115200, SERIAL_8N1, RXD2, TXD2);

    // Initialize I2C for distance sensors
    Wire.begin(SDA_PIN, SCL_PIN, 100000); // Set I2C speed to 100kHz
    delay(200);  // Allow time for the I2C bus to stabilize

    // Initialize first sensor (default address 0x29)
    if (!lox1.begin(0x29)) {
        Serial.println(F("Failed to boot VL53L0X #1"));
        while (1);
    }
    Serial.println("VL53L0X #1 initialized");

    // Initialize second sensor (default address 0x29, change to 0x30)
    if (!lox2.begin(0x29)) {
        Serial.println(F("Failed to boot VL53L0X #2"));
        lox2.setAddress(0x30);  // New I2C address for second sensor
        delay(100); // Wait before retrying
        if (!lox2.begin(0x30)) {
            Serial.println(F("Failed to boot VL53L0X #2 after changing address"));
            while (1);
        }
    }
    Serial.println("VL53L0X #2 initialized");

    stop_table();
}

void loop() {
    // Motor control logic
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
            laptop.println(ramy); // Debugging output
        } else if (ramy == "d") {  // Move backward
            move_up_flag = false;
            move_down_flag = true;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "s") {  // Stop
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "tu") {  // Tilt up
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = true;
            tilt_down_flag = false;
            stop_motion_flag = false;
            laptop.println(ramy); // Debugging output
        } else if (ramy == "td"){  // Tilt down
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = true;
            stop_motion_flag = false;
            laptop.println(ramy); // Debugging output
        } else {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
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

    // Distance sensing logic
    float totalDistance1 = 0;
    float totalDistance2 = 0;

    // Take multiple readings from both sensors and average them
    for (int i = 0; i < NUM_READINGS; i++) {
        VL53L0X_RangingMeasurementData_t measure1;
        VL53L0X_RangingMeasurementData_t measure2;

        // Read sensor 1
        lox1.rangingTest(&measure1, false);
        if (measure1.RangeStatus != 4) {
            totalDistance1 += measure1.RangeMilliMeter;
        } else {
            Serial.println("Sensor 1 out of range");
        }

        // Read sensor 2
        lox2.rangingTest(&measure2, false);
        if (measure2.RangeStatus != 4) {
            totalDistance2 += measure2.RangeMilliMeter;
        } else {
            Serial.println("Sensor 2 out of range");
        }

        delay(CALIBRATION_DELAY);  // Wait before the next reading
    }

    // Calculate average distance for each sensor
    float avgDistance1 = totalDistance1 / NUM_READINGS;
    float avgDistance2 = totalDistance2 / NUM_READINGS;

    // Calculate final average distance
    float averageDistance = (avgDistance1 + avgDistance2) / 2.0;

    // Display the average distance
    Serial.print("Sensor 1 Average Distance (mm): ");
    Serial.println(avgDistance1);
    Serial.print("Sensor 2 Average Distance (mm): ");
    Serial.println(avgDistance2);
    Serial.print("Overall Average Distance (mm): ");
    Serial.println(averageDistance);
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