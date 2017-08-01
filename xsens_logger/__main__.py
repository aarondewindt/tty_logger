import serial
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

    print("Logging...")
    write_process = Process(target=write_process_target, args=(data_fifo_path,))
    try:
        with serial_port:
            write_process.start()
            with open(data_fifo_path, "wb") as f:
                while write_process.is_alive():
                    f.write(serial_port.read(chunk_size))
    except (KeyboardInterrupt, SystemExit, BrokenPipeError):
        if write_process.is_alive():
            write_process.join()
        print("Done")


if __name__ == "__main__":
    main()
