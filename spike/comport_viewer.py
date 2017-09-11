from serial.tools import list_ports

for n, l in enumerate(list_ports.comports(), 1):
    print(n, " : ".join(l))