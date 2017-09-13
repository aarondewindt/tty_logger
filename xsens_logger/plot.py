# This file is used to plot the data
# Converting data is done through sim_common

import matplotlib.pyplot as plt
import pickle
import numpy as np

with open("xsens_log_18.pickle", "rb") as f:
    tables = pickle.load(f)

    tables['packet_counter_diff'] = {'time': None, 'data': None}
    tables['packet_counter_diff']['time'] = tables['packet_counter']['time'][:-1]
    tables['packet_counter_diff']['data'] = np.diff(tables['packet_counter']['data'])

    tables['sampling_frequency'] = {'time': None, 'data': None}
    tables['sampling_frequency']['time'] = tables['packet_counter']['time'][:-1]
    tables['sampling_frequency']['data'] = 1./np.diff(tables['packet_counter']['time'])

    for key, content in tables.items():
        print(key)
        if isinstance(content, dict):
            fig = plt.figure()
            fig.suptitle(key)
            plt.plot(content['time'], content['data'])

    plt.show()
