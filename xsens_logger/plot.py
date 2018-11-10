import matplotlib.pyplot as plt
from sim_common import File
import numpy as np


tables = File("../oct_31.msgp/chunk_96.msgp.gz").load()
# File("../test_7/chunk_160.mat").dump(tables)

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
