import serial
import time 

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ramy = "ramy8"
print("ramy =", ramy)
arduino.write(ramy.encode())
time.sleep(4)

response = arduino.readline()
print(response)