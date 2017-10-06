from functools import partial
import os


def write_process_target(data_fifo_path, data_log_path):
    with open(data_fifo_path, "rb") as fifo:
        with open(data_log_path, "wb") as f:
            try:
                for chunk in iter(partial(fifo.read, 1024), b''):
                    f.write(chunk)
            except (KeyboardInterrupt, SystemExit):
                print("\nLogging stopped.")
                # for chunk in iter(partial(fifo.read, 1024), b''):
                #     print(chunk)
                #     f.write(chunk)
    print("Data logged in '{}'.".format(data_log_path))
    os.unlink(data_fifo_path)
