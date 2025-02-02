#include <WiFi.h>
#include <PubSubClient.h>

// Wi-Fi and MQTT Settings
const char* ssid = "RaspberryPi_Hotspot";
const char* password = "yourpassword";
const char* mqtt_server = "192.168.4.1";  // Change to your Raspberry Pi's IP if different

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* message, unsigned int length) {
    String command = "";
    for (int i = 0; i < length; i++) {
        command += (char)message[i];
    }

    Serial.println("Received Command: " + command);

    if (command == "up") Serial.println("Raising Table...");
    else if (command == "down") Serial.println("Lowering Table...");
    else if (command == "tilt_up") Serial.println("Tilting Table Up...");
    else if (command == "tilt_down") Serial.println("Tilting Table Down...");
    else Serial.println("Unknown command received.");
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP32_Client")) {
            Serial.println("connected!");
            client.subscribe("table/control");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" trying again in 5 seconds...");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { 
        delay(500);
        Serial.print("."); 
    }
    Serial.println("\nConnected to Wi-Fi!");

    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

    reconnect();
}

void loop() {
    if (!client.connected()) reconnect();
    client.loop();
}
