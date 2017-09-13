from serial.tools import list_ports
from serial.serialutil import SerialException
import serial


for n, l in enumerate(list_ports.comports(), 1):
    print(n," : ".join(l))
    