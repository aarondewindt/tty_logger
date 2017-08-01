import matplotlib.pyplot as plt
import pickle
import numpy as np


with open("xsens_log_1.pickle", "rb") as f:
    tables = pickle.load(f)

    tables['packet_counter_diff'] = {'time': None, 'data': None}

    print(tables['packet_counter']['time'])

    tables['packet_counter_diff']['time'] = tables['packet_counter']['time'][:-1]
    tables['packet_counter_diff']['data'] = np.diff(tables['packet_counter']['data'])

    for key, content in tables.items():
        print(key)
        fig = plt.figure()
        fig.suptitle(key)
        plt.plot(content['time'], content['data'])

    plt.show()
