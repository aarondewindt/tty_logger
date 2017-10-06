# In this file we use commands to get the Xsense data and writes all the data
# the Xsense sends to a file

# serial port is an interface through which information transfers on bit at a time
from serial.tools import list_ports
import os
from xsens_logger.xsens import Xsens


def main():
    # baudrate specifies how fast data is sent over in a serial line
    baudrate = 2000000
    xsenses = []

    log_count = get_log_count()

    # enumerate over the list of comports and search for the new Xsense and the old Xsense
    # add the Xsenses to the list xsenses
    for n, (port, desc, hwid) in enumerate(list_ports.comports(), 1):
        if "MTi-100" in desc:
            xsenses.append(Xsens(len(xsenses), port, baudrate, log_count))
 
    if len(xsenses) == 0:
        raise Exception("Xsens not found.")

    print("Logging...")

    for xsens in xsenses:
        xsens.request_device_id()

    try:
        while all(map(lambda x: x.write_process.is_alive(), xsenses)):
            for xsens in xsenses:
                xsens.read_chunk()
    except (KeyboardInterrupt, SystemExit, BrokenPipeError):
        for xsens in xsenses:
            if xsens.write_process.is_alive():
                xsens.write_process.join()
        print("Done")


def get_log_count():
    log_count_path = "log_count.txt"
    if not os.path.isfile(log_count_path):
        log_count = 0
    else:
        with open(log_count_path, "r") as f:
            try:
                log_count = int(f.read()) + 1
            except ValueError:
                log_count = 0

    with open(log_count_path, "w") as f:
        f.write(str(log_count))

    return log_count


if __name__ == "__main__":
    main()
