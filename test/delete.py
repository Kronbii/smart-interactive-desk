import serial  # for connection with the serial port

# To connect to the serial port
import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())  # outputs all the ports connected
found_port = list()  # list of all the ports connected
connection = False  # flag, set it to True when you find your port

for i in range(len(ports)):
    print(ports[i])  # to print all the available ports connected
    if "USB" in ports[i].device:
        found_port.append(ports[i].device)  # append all the ports which have serial word in them
        print(found_port[i])
