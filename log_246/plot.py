import matplotlib.pyplot as plt
from sim_common import flex_load, flex_dump
import numpy as np


def load_file(path):
    tables = flex_load(path)
    # File("../test_7/chunk_160.mat").dump(tables)

    tables['packet_counter_diff'] = {'time': None, 'data': None}
    tables['packet_counter_diff']['time'] = tables['packet_counter']['time'][:-1]
    tables['packet_counter_diff']['data'] = np.diff(tables['packet_counter']['data'])

    tables['sampling_frequency'] = {'time': None, 'data': None}
    tables['sampling_frequency']['time'] = tables['packet_counter']['time'][:-1]
    tables['sampling_frequency']['data'] = 1./np.diff(tables['packet_counter']['time'])
    tables.pop('device_id')
    return tables

x0 = load_file("x0_60.msgp.gz")
x1 = load_file("x1_60.msgp.gz")

# print(list(x0.keys()))
# print(x0['device_id'])
# raise SystemExit(0)

flex_dump(x0, "x0_60.mat")
flex_dump(x1, "x1_60.mat")

for key, content_x0 in x0.items():
    print(key)
    content_x1 = x1[key]
    print(np.isclose(content_x0['data'], content_x1['data']).all())
    if isinstance(content_x0, dict):
        fig = plt.figure()
        fig.suptitle(key)
        plt.plot(content_x0['time'], content_x0['data'])
        plt.plot(content_x1['time'], content_x1['data'])
        # fig.legends()
plt.show()
