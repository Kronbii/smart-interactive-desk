#include <HardwareSerial.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>

// Stepper motor pins
#define M1IN1 5
#define M1IN2 4
#define M2IN1 3
#define M2IN2 2

#define btmSwitch 19  // Bottom switch pin

#define RPWM 7   // Right PWM
#define LPWM 6   // Left PWM

// Direction and movement flags
bool move_up_flag = false;
bool move_down_flag = false;
bool tilt_up_flag = false;
bool tilt_down_flag = false;
bool stop_motion_flag = true;
bool btm_limit_flag = false;  // Only the bottom limit flag now

// Debouncing variables
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 200; // Debounce delay (in milliseconds)

// LCD pin connections (updated)
#define PIN_RST  8    // Reset pin for the LCD
#define PIN_CE   9    // Chip Enable pin for the LCD
#define PIN_DC   10   // Data/Command pin for the LCD
#define PIN_DIN  11   // Serial Data pin for the LCD
#define PIN_CLK  12 

Adafruit_PCD8544 display = Adafruit_PCD8544(PIN_CLK, PIN_DIN, PIN_DC, PIN_CE, PIN_RST);


void setup() {
    pinMode(M1IN1, OUTPUT);
    pinMode(M1IN2, OUTPUT);
    pinMode(M2IN1, OUTPUT);
    pinMode(M2IN2, OUTPUT);
    
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);

    pinMode(btmSwitch, INPUT_PULLUP); // Set bottom switch pin as input with internal pull-up resistor

    display.begin();
    display.setContrast(60);  //contrast (0-100)
    display.clearDisplay();


    Serial2.begin(115200);
    Serial.begin(115200);    // Main serial communication

    attachInterrupt(digitalPinToInterrupt(btmSwitch), btm_int, FALLING);  // Trigger on pin 19 falling edge (button press)

    stop_table();
    Serial.println("Begin of operations");

}

void loop() {
    // Handle bottom limit switch interrupt
    if (btm_limit_flag) {
        stop_table();
        Serial.println("Bottom Interrupt Registered");
        stop_table();  // Stop all movements if the table is frozen
        delay(1000);   // Wait for a moment
        move_table_up();
        delay(2000);   // Wait for a moment
        stop_table();
        btm_limit_flag = false;
    }
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(BLACK);
    display.setCursor(0, 10);


    // Read and handle commands from Serial2 (remote control)
    if (Serial.available() > 0) {
        String ramy = Serial.readStringUntil('\n');  // Read full command
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

    // Execute movements based on flags
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

    display.display();
    

}

// Bottom limit switch interrupt (with debouncing)
void btm_int() {
    unsigned long currentMillis = millis();
    if (currentMillis - lastDebounceTime > debounceDelay) {  // Only trigger if debounce time has passed
        stop_table();
        Serial.println("Bottom Interrupt Function Entered");
        btm_limit_flag = true;
        lastDebounceTime = currentMillis;  // Update last debounce time
    }
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