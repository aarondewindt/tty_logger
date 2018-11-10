import matplotlib.pyplot as plt
from sim_common import File
import numpy as np

print("Loading data...")
chunk_tables = [
    File("./oct_31.msgp/chunk_94.msgp.gz").load(),
    File("./oct_31.msgp/chunk_95.msgp.gz").load(),
    File("./oct_31.msgp/chunk_96.msgp.gz").load(),
]

print("Joining data...")
joined_tables = dict([[k, {'time': [], 'data': []}] for k in chunk_tables[0].keys()])
for i, tables in enumerate(chunk_tables):
    for key in tables.keys():
        if key != "device_id":
            print(f"  {i}: {key}")
            joined_tables[key]['time'] += list(tables[key]['time'])
            joined_tables[key]['data'] += list(tables[key]['data'])

print(f"Calculating package counter diff...")
joined_tables['packet_counter_diff'] = {'time': None, 'data': None}
joined_tables['packet_counter_diff']['time'] = joined_tables['packet_counter']['time'][:-1]
joined_tables['packet_counter_diff']['data'] = np.diff(joined_tables['packet_counter']['data'])

print(f"Calculating sampling frequency...")
joined_tables['sampling_frequency'] = {'time': None, 'data': None}
joined_tables['sampling_frequency']['time'] = joined_tables['packet_counter']['time'][:-1]
joined_tables['sampling_frequency']['data'] = 1. / np.diff(joined_tables['packet_counter']['time'])

print("Saving data")

File("./xsens_oct_31.mat").dump(joined_tables)

print("Plotting...")
for key, content in joined_tables.items():
    print(" -", key)
    if isinstance(content, dict):
        fig = plt.figure()
        fig.suptitle(key)
        plt.plot(content['time'], content['data'])

plt.show()
