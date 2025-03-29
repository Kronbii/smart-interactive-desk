#!/bin/bash

# Set your Bluetooth device MAC address here
DEVICE_MAC="90:89:5F:21:D4:94"  # Replace with your device's MAC address

# Function to check if Bluetooth is powered on
check_bluetooth_power() {
    STATUS=$(bluetoothctl show | grep "Powered: yes")
    if [ -z "$STATUS" ]; then
        echo "Bluetooth is off. Turning it on..."
        bluetoothctl power on
        sleep 2
    fi
}

# Function to check if the device is already connected
check_device_connection() {
    CONNECTED=$(bluetoothctl info "$DEVICE_MAC" | grep "Connected: yes")
    if [ ! -z "$CONNECTED" ]; then
        echo "Device $DEVICE_MAC is already connected."
        exit 0
    fi
}

# Enable Bluetooth if it's off
check_bluetooth_power

# Ensure the device is trusted and paired
echo "Checking if the device is paired..."
PAIRED=$(bluetoothctl info "$DEVICE_MAC" | grep "Paired: yes")

if [ -z "$PAIRED" ]; then
    echo "Pairing with $DEVICE_MAC..."
    bluetoothctl pair "$DEVICE_MAC"
    sleep 2
fi

# Trust the device
echo "Trusting device..."
bluetoothctl trust "$DEVICE_MAC"
sleep 1

# Attempt to connect
echo "Connecting to device $DEVICE_MAC..."
bluetoothctl connect "$DEVICE_MAC"

# Verify connection
check_device_connection

echo "Bluetooth connection setup complete."
exit 0
