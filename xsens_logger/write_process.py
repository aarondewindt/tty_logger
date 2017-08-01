from functools import partial
import datetime
import os


def write_process_target(data_fifo_path):
    log_file_path = os.path.abspath("./xsens_log_{}.bin".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    print("Writing to '{}'".format(log_file_path))

    with open(data_fifo_path, "rb") as fifo:
        with open(log_file_path, "wb") as f:
            try:
                for chunk in iter(partial(fifo.read, 1024), ''):
                    f.write(chunk)
            except (KeyboardInterrupt, SystemExit):
                pass
    print("Data dumped in '{}'.".format(log_file_path))
    os.unlink(data_fifo_path)
