# In this file we use commands to get the Xsense data and writes all the data
# the Xsense sends to a file

# serial port is an interface through which information transfers on bit at a time
import serial 
from time import sleep
from serial.tools import list_ports
from io import BytesIO

import os
from multiprocessing import Process
from xsens_logger.write_process import write_process_target

def main():
    # baudrate specifies how fast data is sent over in a serial line
    # os.path.abspath(a) creates a new path called a
    baudrate = 2000000
    xsens_info = None
    data_fifo_path = os.path.abspath("./data_fifo")
    chunk_size = 1024
    counter = 0
    p=1
  
    xsenses = []
    data_fifo_paths = []
    serial_ports = []
    write_processes = []
    
 
 

    # enumerate over the list of comports and search for the new Xsense and the old Xsense
    # add the Xsenses to the list xsenses
    while len(xsenses) < p:
        print("Looking for new Xsense...")
        for n, (port, desc, hwid) in enumerate(list_ports.comports(), 1):
            if "SER=01782017" in hwid:
                xsenses.append((port, desc, hwid, n))
                break
        print("Looking for old Xsens...\n")
        for n, (port, desc, hwid) in enumerate(list_ports.comports(), 1):
            if "SER=017006FE" in hwid:
                xsenses.append((port, desc, hwid, n))
                break
        counter += 1

    # Print Xsense info
    print("Xsense1: '{}'".format(xsenses[0]))
    print("Xsense2: '{}'\n".format(xsenses[1]))
 
 
    if len(xsenses) ==  0:
        raise Exception("Xsens and mockup_Xsense not found.")


    for i, xsense in enumerate(xsenses):
        data_fifo_paths.append("./data_fifo_{}".format(i))
        if os.path.exists(data_fifo_path):
            os.unlink(data_fifo_path)
        os.mkfifo(data_fifo_path)
        
        print(data_fifo_paths)
   
        # Connect to new Xsense at '/dev/ttyUSB0', port = xsenses[0][0] full device name
        # Connect to old Xsense at '/dev/ttyUSB2', port = xsenses[1][0] full device name 
        print("Connecting to sensor at '{}'...".format(xsenses[i][0]))
               
        if not os.path.isfile("log_count.txt"):
                log_count = 0
        else:
            with open("log_count.txt", "r") as f:
                try:
                    log_count = int(f.read()) + 1
                except ValueError:
                    log_count = 0

        with open("log_count.txt", "w") as f:
            f.write(str(log_count))
        
        # Open serial port
        serial_port = serial.Serial(xsenses[i][0], baudrate, timeout=0)
        serial_ports.append(serial_port)
        print(serial_ports)
        
        write_process = Process(target=write_process_target, args=(data_fifo_paths[i]))
        write_processes.append(write_process)
        print(write_processes)
        
        
        with serial_port:
            n_bytes_to_skip = 20000
            while n_bytes_to_skip > 0:
                n_bytes_to_skip -= len(serial_port.read(chunk_size))  
        

        # process opstarten.
        # data fifo openen.
        # Bytes skippen
        # Vraag voor device id
        # try: while alive
    


 
 
 
 
'''  
    try:
        with serial_port:
            n_bytes_to_skip = 20000
            while n_bytes_to_skip > 0:
                n_bytes_to_skip -= len(serial_port.read(chunk_size))
        
            
            write_process.start()
            # Create a file object for writing/reading/appending in binary format
            with open(data_fifo_path, "wb") as f:

                # Reset xsens
                # serial_port.write(b'\xfa\xff\x40\x00\xc1')
                # serial_port.flush()
                # sleep(0.5)

                # Goto configuration mode
                serial_port.write(b'\xfa\xff\x30\x00\xd1')
                serial_port.flush()
                sleep(0.1)

                # Request device ID
                serial_port.write(b'\xfa\xff\x00\x00\x01')
                serial_port.flush()
                sleep(0.1)

                f.write(serial_port.read(chunk_size))

                # Goto measurement mode
                serial_port.write(b'\xfa\xff\x10\x00\xf1')
                serial_port.flush()

                print("Logging...")

                while write_process.is_alive():
                    for serial, data_fifo in zip(serial_list, data_fifo_list):
                        f.write(serial_port.read(chunk_size))

    except (KeyboardInterrupt, SystemExit, BrokenPipeError):
        if write_process.is_alive():
            write_process.join()
        print("Done")
    
'''
    
    
if __name__ == "__main__":
    main()
