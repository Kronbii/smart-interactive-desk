import paho.mqtt.client as mqtt
import time

# MQTT Broker (Raspberry Pi's IP Address)
MQTT_BROKER = "192.168.4.1"  # Change to your Raspberry Pi's IP if different
MQTT_TOPIC = "table/control"

# Initialize MQTT Client
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    print("\nCommand Options:")
    print(" 1 - Raise Table")
    print(" 2 - Lower Table")
    print(" 3 - Tilt Table Up")
    print(" 4 - Tilt Table Down")
    print(" 5 - Exit")

    choice = input("Enter command: ")

    if choice == "1":
        client.publish(MQTT_TOPIC, "up")
        print("Command sent: Raising Table...")
    elif choice == "2":
        client.publish(MQTT_TOPIC, "down")
        print("Command sent: Lowering Table...")
    elif choice == "3":
        client.publish(MQTT_TOPIC, "tilt_up")
        print("Command sent: Tilting Table Up...")
    elif choice == "4":
        client.publish(MQTT_TOPIC, "tilt_down")
        print("Command sent: Tilting Table Down...")
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid option, please enter a number between 1 and 5.")

    time.sleep(1)  # Small delay to prevent flooding

client.disconnect()
