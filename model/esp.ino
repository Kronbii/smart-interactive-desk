#include "bemo.h"

SerialComm comm;
MotionControl motion;
TableStatus table;
Adafruit_PCD8544 display = Adafruit_PCD8544(PIN_DC, PIN_CS, PIN_RST);


String command;
String last_command;
bool move_up_flag = false;
bool move_down_flag = false;
bool tilt_up_flag = false;
bool tilt_down_flag = false;
bool stop_motion_flag = true;
double height;
int disp_height;

void setID() {
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(10);
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, LOW);

  if (!lox1.begin(LOX1_ADDRESS)) {
    Serial.println(F("Failed to boot first VL53L0X"));
    while (1);
  }
  delay(10);

  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  if (!lox2.begin(LOX2_ADDRESS)) {
    Serial.println(F("Failed to boot second VL53L0X"));
    while (1);
  }
}

void setup() {
    digitalWrite(52, HIGH);
    comm.begin(115200);
    motion.init();
    table.init();

    HCSR04.begin(12, 22);

    pinMode(man_up_pin, INPUT_PULLUP);
    pinMode(man_down_pin, INPUT_PULLUP);
    pinMode(man_tilt_up_pin, INPUT_PULLUP);
    pinMode(man_tilt_down_pin, INPUT_PULLUP);

    pinMode(PIN_DC, OUTPUT);
    pinMode(PIN_CS, OUTPUT);
    pinMode(PIN_RST, OUTPUT);

    Serial.println(F("Starting..."));
    //setID();
    
    motion.stop();
    //read_dual_sensors(sensor1, sensor2);
    Serial.println("Begin of operations");

    display.begin();
    display.setContrast(60);  // Adjust this if screen is blank or too dim
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(BLACK);
    display.setCursor(0, 0);
    display.println("Hello Mega!");
    display.display();

    height = HCSR04.measureDistanceCm()[0];
    disp_height = int(height);
    pinMode(52, OUTPUT);
}

void loop() {
  display.clearDisplay();         // Clear old frame
  display.setCursor(0, 16);
  display.setTextSize(2);
  display.setTextColor(BLACK);
  
  height = HCSR04.measureDistanceCm()[0];
  for (int i=0; i<NUM_SAMPLES; i++){
    height = height + HCSR04.measureDistanceCm()[0];
  }

  height = height/ NUM_SAMPLES;
  disp_height = int(height);

  Serial.println(height);
  display.println(disp_height);
  display.display();

  bool man_up = digitalRead(man_up_pin);
  bool man_down = digitalRead(man_down_pin);
  bool man_tilt_up = digitalRead(man_tilt_up_pin);
  bool man_tilt_down = digitalRead(man_tilt_down_pin);

  if(man_up == LOW && man_down == LOW){
    Serial.println("RESETING");
    digitalWrite(52, LOW);
  }
  else if (man_up == LOW) {
    command = "u";
    manual_active = true;
  } else if (man_down == LOW) {
    command = "d";
    manual_active = true;
  } else if (man_tilt_up == LOW) {
    command = "tu";
    manual_active = true;
  } else if (man_tilt_down == LOW) {
    command = "td";
    manual_active = true;
  } else if (manual_active) {
    // A manual button was just released → send stop
    command = "s";
    manual_active = false; // reset
  } else {
    // No manual input → fallback to remote
    comm.readCommand(command);
  }

  delay(100);

  if (command != last_command) {
    if (command == "u") {
      move_up_flag = true; move_down_flag = tilt_up_flag = tilt_down_flag = false;
      stop_motion_flag = false; last_command = command;
    } else if (command == "d") {
      move_down_flag = true; move_up_flag = tilt_up_flag = tilt_down_flag = false;
      stop_motion_flag = false; last_command = command;
    } else if (command == "s") {
      move_up_flag = move_down_flag = tilt_up_flag = tilt_down_flag = false;
      stop_motion_flag = true; last_command = command;
    } else if (command == "tu") {
      tilt_up_flag = true; move_up_flag = move_down_flag = tilt_down_flag = false;
      stop_motion_flag = false; last_command = command;
    } else if (command == "td") {
      tilt_down_flag = true; move_up_flag = move_down_flag = tilt_up_flag = false;
      stop_motion_flag = false; last_command = command;
    } else {
      command = last_command;
    }
  }

    if(move_up_flag && height > 100){
        move_up_flag = false;
    }
    if(move_down_flag && height < 80){
        move_down_flag = false;
    }

  if (move_up_flag && !stop_motion_flag) {
    motion.moveUp(); 
  } else if (move_down_flag && !stop_motion_flag) {
    motion.moveDown();
  } else if (tilt_up_flag && !stop_motion_flag) {
    motion.tiltUp();
  } else if (tilt_down_flag && !stop_motion_flag) {
    motion.tiltDown();
  } else {
    motion.stop();
  }

}