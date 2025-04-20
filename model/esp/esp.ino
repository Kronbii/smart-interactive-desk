#include "bemo.h"

SerialComm comm;
MotionControl motion;
TableStatus table;

String command;
String last_command;
bool move_up_flag = false;
bool move_down_flag = false;
bool tilt_up_flag = false;
bool tilt_down_flag = false;
bool stop_motion_flag = true;

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
    comm.begin(115200);
    motion.init();
    table.init();

    HCSR04.begin(12, 22);

    pinMode(man_up_pin, INPUT_PULLUP);
    pinMode(man_down_pin, INPUT_PULLUP);
    pinMode(man_tilt_up_pin, INPUT_PULLUP);
    pinMode(man_tilt_down_pin, INPUT_PULLUP);

    Serial.println(F("Starting..."));
    //setID();
    
    motion.stop();
    //read_dual_sensors(sensor1, sensor2);
    Serial.println("Begin of operations");
}

void loop() {
  double height = HCSR04.measureDistanceCm()[0];
  Serial.println(height);

  bool man_up = digitalRead(man_up_pin);
  bool man_down = digitalRead(man_down_pin);
  bool man_tilt_up = digitalRead(man_tilt_up_pin);
  bool man_tilt_down = digitalRead(man_tilt_down_pin);

  if (man_up == LOW) {
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