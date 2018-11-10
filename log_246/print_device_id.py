from sim_common import flex_load

x0 = flex_load("x0_0.msgp.gz")
x1 = flex_load("x1_0.msgp.gz")

print(x0['device_id'])
print(x1['device_id'])
