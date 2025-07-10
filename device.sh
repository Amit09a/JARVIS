#!/bin/zsh

# Disconnecting old connections...
echo "Disconnecting old connections..."
adb disconnect

# Setting up connected device
echo "Setting up connected device..."
adb tcpip 5555

# Waiting for device to initialize
echo "Waiting for device to initialize..."
sleep 3

# Get the full IP address (with subnet) of wlan0
ipfull=$(adb shell ip addr show wlan0 | grep 'inet ' | awk '{print $2}')

# Extract just the IP part (before the slash)
ip=$(echo "$ipfull" | cut -d/ -f1)

# Connecting to device with IP
echo "Connecting to device with IP $ip..."
adb connect "$ip"

# -----------------------------------
# Manual connection section (optional)
# -----------------------------------

# Set the IP address of your Android device manually (if needed)
DEVICE_IP="192.168.1.3"

# Set the port number for ADB
ADB_PORT=5555

# Set the path to the ADB executable (assuming it's in PATH)
ADB_PATH="adb"

# Restart the ADB server
$ADB_PATH kill-server
$ADB_PATH start-server

# Connect to the Android device over Wi-Fi using manual IP
$ADB_PATH connect "$DEVICE_IP:$ADB_PORT"
