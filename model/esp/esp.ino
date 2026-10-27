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
double height, angle;
int disp_angle;
int disp_height;

NewPing sonar[SONAR_NUM] = {
  NewPing(HEIGHT_TRIG, HEIGHT_ECHO, MAX_DISTANCE),  // Sensor 0
  NewPing(TILT_TRIG, TILT_ECHO, MAX_DISTANCE)   // Sensor 1
};

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
  delay(2000);
    digitalWrite(ARDRST, HIGH);
    comm.begin(115200);
    motion.init();
    table.init();

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
    display.setTextSize(2);
    display.setTextColor(BLACK);
    display.setCursor(0, 0);
    display.println("WELCOME BEMO");
    display.display();

    height = sonar[0].ping_cm();
    angle = sonar[1].ping_cm();
    pinMode(ARDRST, OUTPUT);
}

void loop() {
  display.clearDisplay();         // Clear old frame
  
  height = sonar[0].ping_cm();
  angle = sonar[1].ping_cm();

  for (int i=0; i<NUM_SAMPLES; i++){
    height = height + sonar[0].ping_cm();
    angle = angle + sonar[1].ping_cm();
  }

  height = height/ NUM_SAMPLES;
  angle = angle / NUM_SAMPLES;
  angle = atan2(angle, BASE) * 180.0 / PI;
  disp_height = int(height);
  disp_angle = int(angle);

  String heightStr = String(disp_height) + " cm";  // Rounded to int
  String tiltStr = String(disp_angle) + " deg";

  display.setTextSize(2);
  display.setTextColor(BLACK);

  if (height >= 100){
    display.setCursor(6, 4);
  }
  else{
    display.setCursor(18, 4);
}
  
  Serial.print("Height: ");
  Serial.print(height);
  Serial.print(" cm, Angle: ");
  Serial.print(angle);
  Serial.println(" deg");
  display.println(heightStr);

  display.setCursor(12, 28);
  display.println(tiltStr);
  display.display();

  bool man_up = digitalRead(man_up_pin);
  bool man_down = digitalRead(man_down_pin);
  bool man_tilt_up = digitalRead(man_tilt_up_pin);
  bool man_tilt_down = digitalRead(man_tilt_down_pin);

  if(man_up == LOW && man_down == LOW){
    Serial.println("RESETING");
    digitalWrite(ARDRST, LOW);
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