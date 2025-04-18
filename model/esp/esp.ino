#include <HardwareSerial.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include "Adafruit_VL53L0X.h"

// address we will assign if dual sensor is present
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31

// set the pins to shutdown
#define SHT_LOX1 9
#define SHT_LOX2 8

// objects for the vl53l0x
Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();

// this holds the measurement
VL53L0X_RangingMeasurementData_t measure1;
VL53L0X_RangingMeasurementData_t measure2;

int sensor1 = 0;
int sensor2 = 0;

String command;
String last_command;

// Stepper motor pins
#define M1IN1 5
#define M1IN2 4
#define M2IN1 3
#define M2IN2 2

#define RPWM 7   // Right PWM
#define LPWM 6   // Left PWM

// Direction and movement flags
bool move_up_flag = false;
bool move_down_flag = false;
bool tilt_up_flag = false;
bool tilt_down_flag = false;
bool stop_motion_flag = true;
bool btm_limit_flag = false;  // Only the bottom limit flag now

// LCD pin connections (updated)
#define PIN_RST  8    // Reset pin for the LCD
#define PIN_CE   9    // Chip Enable pin for the LCD
#define PIN_DC   10   // Data/Command pin for the LCD
#define PIN_DIN  11   // Serial Data pin for the LCD
#define PIN_CLK  12 

Adafruit_PCD8544 display = Adafruit_PCD8544(PIN_CLK, PIN_DIN, PIN_DC, PIN_CE, PIN_RST);

void setID() {
  // all reset
  digitalWrite(SHT_LOX1, LOW);    
  digitalWrite(SHT_LOX2, LOW);
  delay(10);
  // all unreset
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  // activating LOX1 and resetting LOX2
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, LOW);

  // initing LOX1
  if(!lox1.begin(LOX1_ADDRESS)) {
    Serial.println(F("Failed to boot first VL53L0X"));
    while(1);
  }
  delay(10);

  // activating LOX2
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  //initing LOX2
  if(!lox2.begin(LOX2_ADDRESS)) {
    Serial.println(F("Failed to boot second VL53L0X"));
    while(1);
  }
}

void read_dual_sensors(int &sensor1Reading, int &sensor2Reading) {
    lox1.rangingTest(&measure1, false); // pass in 'true' to get debug data printout!
    lox2.rangingTest(&measure2, false); // pass in 'true' to get debug data printout!
    
    // Store sensor one reading
    sensor1Reading = (measure1.RangeStatus != 4) ? measure1.RangeMilliMeter : -1;
    
    // Store sensor two reading
    sensor2Reading = (measure2.RangeStatus != 4) ? measure2.RangeMilliMeter : -1;
}

void rec_data(String &command) {
    // Read and handle commands from Serial2 (remote control)
    if (Serial.available() > 0) {
        command = Serial.readStringUntil('\n');  // Read full command
        command = command.trim();  // Remove whitespace and newline
    }
}

void set_flags(String &command, String &last_command, bool &move_up_flag, bool &move_down_flag, bool &tilt_up_flag, bool &tilt_down_flag, bool &stop_motion_flag) {
    if (command != last_command){
        if (command == "u") {
            move_up_flag = true;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            last_command = command;
        } else if (command == "d") {
            move_up_flag = false;
            move_down_flag = true;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = false;
            last_command = command;
        } else if (command == "s") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = false;
            stop_motion_flag = true;
            last_command = command;
        } else if (command == "tu") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = true;
            tilt_down_flag = false;
            stop_motion_flag = false;
            last_command = command;
        } else if (command == "td") {
            move_up_flag = false;
            move_down_flag = false;
            tilt_up_flag = false;
            tilt_down_flag = true;
            stop_motion_flag = false;
            last_command = command;
        } else {
            command = last_command;
        }
    }
}

void perform_command() {
    if (move_up_flag && !stop_motion_flag) {
        move_table_up();
        display.print("Going Up");
    } else if (move_down_flag && !stop_motion_flag) {
        move_table_down();
        display.print("Going down");
    } else if (tilt_up_flag && !stop_motion_flag) {
        tilt_table_up();
        display.print("tilting Up");
    } else if (tilt_down_flag && !stop_motion_flag) {
        tilt_table_down();
        display.print("tilting down");
    } else {
        stop_table();
        display.print("BEMO waiting");
    }
}

void setup() {
    pinMode(M1IN1, OUTPUT);
    pinMode(M1IN2, OUTPUT);
    pinMode(M2IN1, OUTPUT);
    pinMode(M2IN2, OUTPUT);
    
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);

    display.begin();
    display.setContrast(60);  //contrast (0-100)
    display.clearDisplay();

    Serial.begin(115200);    // Main serial communication

    while (! Serial) { delay(1); }

    pinMode(SHT_LOX1, OUTPUT);
    pinMode(SHT_LOX2, OUTPUT);

    Serial.println(F("Shutdown pins inited..."));

    digitalWrite(SHT_LOX1, LOW);
    digitalWrite(SHT_LOX2, LOW);

    Serial.println(F("Both in reset mode...(pins are low)"));
  
    Serial.println(F("Starting..."));
    setID();

    stop_table();
    Serial.println("Begin of operations");
}

void loop() {

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(BLACK);
    display.setCursor(0, 10);

    rec_data(command);
    set_flags(command, last_command, move_up_flag, move_down_flag, tilt_up_flag, tilt_down_flag, stop_motion_flag);
    perform_command();
    read_dual_sensors(sensor1, sensor2);  // Read sensor values
    // add sensor limit
    display.display();
}

// Motor control functions
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
