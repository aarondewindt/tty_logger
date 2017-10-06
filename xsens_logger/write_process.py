from functools import partial
import os
from tqdm import tqdm


def write_process_target(data_fifo_path, id, log_count):
    s = os.statvfs(os.path.dirname(data_fifo_path))
    available_memory = s.f_frsize * s.f_bavail


    log_file_path = os.path.abspath("./xsens_log_{}.bin".format(log_count))
    # print("Writing to '{}'".format(log_file_path))

    with open(data_fifo_path, "rb") as fifo:
        with open(log_file_path, "wb") as f:
            try:
                for chunk in iter(partial(fifo.read, 1024), b''):
                    f.write(chunk)
            except (KeyboardInterrupt, SystemExit):
                print("\nLogging stopped, writing the remaining bytes in the buffer...")
                for chunk in iter(partial(fifo.read, 1024), b''):
                    f.write(chunk)
    print("Data dumped in '{}'.".format(log_file_path))
    os.unlink(data_fifo_path)
