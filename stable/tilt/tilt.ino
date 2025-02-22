#define STEP1 3  // Step pin for Motor 1
#define DIR1 2   // Direction pin for Motor 1
#define STEP2 5  // Step pin for Motor 2
#define DIR2 4   // Direction pin for Motor 2

#define BTN_CW 6   // Button for clockwise rotation
#define BTN_CCW 7  // Button for counterclockwise rotation

#define STEP_DELAY 500  // Microseconds delay between steps

void setup() {
    pinMode(STEP1, OUTPUT);
    pinMode(DIR1, OUTPUT);
    pinMode(STEP2, OUTPUT);
    pinMode(DIR2, OUTPUT);

    pinMode(BTN_CW, INPUT_PULLUP);  // Internal pull-up resistor
    pinMode(BTN_CCW, INPUT_PULLUP); // Internal pull-up resistor
}

void loop() {
    if (digitalRead(BTN_CW) == LOW) {  // Clockwise rotation
        digitalWrite(DIR1, HIGH);
        digitalWrite(DIR2, HIGH);
        rotateBothMotors();
    } 
    else if (digitalRead(BTN_CCW) == LOW) {  // Counterclockwise rotation
        digitalWrite(DIR1, LOW);
        digitalWrite(DIR2, LOW);
        rotateBothMotors();
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