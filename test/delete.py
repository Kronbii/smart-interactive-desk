import serial  # for connection with the serial port

# To connect to the serial port
import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())  # outputs all the ports connected
found_port = list()  # list of all the ports connected
connection = False  # flag, set it to True when you find your port

for i in range(len(ports)):
    print(ports[i])  # to print all the available ports connected
    if "Serial" in ports[i].description:
        found_port.append(i)  # append all the ports which have serial word in them
               
for j in range(len(found_port)):
    serial_port = str(ports[found_port[j]])[:4]  # auto detect the serial port
    try:
        serial_connection = serial.Serial(serial_port, baudrate=9600, timeout=2)
        serial_connection.write('write your command'.encode())
        response = serial_connection.read(1)
        """
        write the comparator code here to confirm the read character, if nothing is read then the timeout
        factor in the code will help to pass this port and try different port.
        if conndition for the Serial is met:
          connection = True
        """

    except:  
      connection = False
      pass

    if connection is True:
      print("port found")
      break