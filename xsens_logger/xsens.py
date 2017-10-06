import os
import serial
from time import sleep
from multiprocessing import Process
from xsens_logger.write_process import write_process_target


class Xsens:
    chunk_size = 1024

    def __init__(self, idx, port, baud, log_count):
        self.port = port
        self.baud = baud
        self.log_count = log_count
        self.idx = idx
        self.data_fifo_path = "./data_fifo_{}.bin".format(self.idx)
        self.data_log_path = "./data_log_{}_{}.bin".format(log_count, self.idx)

        if os.path.exists(self.data_fifo_path):
            os.unlink(self.data_fifo_path)
        os.mkfifo(self.data_fifo_path)

        print("Connecting to sensor at '{}'...".format(self.port))
        self.serial_port = serial.Serial(port, baud, timeout=0)
        # self.serial_port.open()

        n_bytes_to_skip = 20000
        while n_bytes_to_skip > 0:
            n_bytes_to_skip -= len(self.serial_port.read(self.chunk_size))

        self.write_process = Process(target=write_process_target, args=(self.data_fifo_path,
                                                                        self.data_log_path))
        self.write_process.start()

        self.data_fifo = open(self.data_fifo_path, "wb")

    def __del__(self):
        self.serial_port.close()

    def read_chunk(self):
        self.data_fifo.write(self.serial_port.read(self.chunk_size))

    def request_device_id(self):
        # Goto configuration mode
        self.serial_port.write(b'\xfa\xff\x30\x00\xd1')
        self.serial_port.flush()
        sleep(0.1)

        # Request device ID
        self.serial_port.write(b'\xfa\xff\x00\x00\x01')
        self.serial_port.flush()
        sleep(0.1)

        self.data_fifo.write(self.serial_port.read(self.chunk_size))

        # Goto measurement mode
        self.serial_port.write(b'\xfa\xff\x10\x00\xf1')
        self.serial_port.flush()

