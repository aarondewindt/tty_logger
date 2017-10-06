import serial
from serial.tools import list_ports
from os import urandom
from time import sleep

baudrate = 2000000
device_info = None
chunk_size = 54
delay = 0.0005
device_port = "/dev/ttyUSB1"

serial_port = serial.Serial(device_port, baudrate, timeout=0)
print("Connecting to '{}'...".format(device_port))
#serial_port.open()

with serial_port:
    print("Connected...")
    try:
        while True:
            serial_port.write(urandom(chunk_size))
            sleep(delay)
    except:
        pass
