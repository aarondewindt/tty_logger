from functools import partial
import os


def write_process_target(data_fifo_path):

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
