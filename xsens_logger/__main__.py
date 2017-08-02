import serial
from time import sleep

from serial.tools import list_ports
from io import BytesIO
import os
from multiprocessing import Process

from xsens_logger.write_process import write_process_target


def main():
    baudrate = 2000000
    xsens_info = None
    data_fifo_path = os.path.abspath("./data_fifo")
    chunk_size = 1024

    print("Looking for Xsens...")
    for n, (port, desc, hwid) in enumerate(list_ports.comports(), 1):
        if "MTi-100" in desc:
            xsens_info = (port, desc, hwid, n)
            break

    if xsens_info is None:
        raise Exception("Xsens not found.")

    if os.path.exists(data_fifo_path):
        os.unlink(data_fifo_path)
    os.mkfifo(data_fifo_path)

    print("Connecting to Xsens at '{}'...".format(xsens_info[0]))

    serial_port = serial.Serial(xsens_info[0], baudrate, timeout=0)
    write_process = Process(target=write_process_target, args=(data_fifo_path,))
    try:
        with serial_port:
            n_bytes_to_skip = 20000
            while n_bytes_to_skip > 0:
                n_bytes_to_skip -= len(serial_port.read(chunk_size))

            write_process.start()
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
                    f.write(serial_port.read(chunk_size))

    except (KeyboardInterrupt, SystemExit, BrokenPipeError):
        if write_process.is_alive():
            write_process.join()
        print("Done")


if __name__ == "__main__":
    main()
