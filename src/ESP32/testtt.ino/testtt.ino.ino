
void move_table_up(){
    Serial.println("Moving table up");
}

void move_table_down(){
    Serial.println("Moving table down");
}

void tilt_table_up(){
    Serial.println("Tilting table up");
}

void tilt_table_down(){
    Serial.println("Tilting table down");
}

void setup(){
    Serial.begin(9600);
}

void loop(){
    if (Serial.available() > 0) {
        char input = Serial.read();
        Serial.print("You entered: ");
        Serial.println(input);

    input = tolower(input);

    if (input == 'w'){
        move_table_up();
    }
    else if (input == 's'){
        move_table_down();
    }
    else if (input == 'a'){
        tilt_table_up();
    }
    else if (input == 'd'){
        tilt_table_down();
    }
    }
}