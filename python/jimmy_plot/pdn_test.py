import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math

from file_read_backwards import FileReadBackwards
import os, util
from functools import reduce

class PDN:
    def __init__(self, L, C, R, VDC, CLK):
        self.L = L
        self.C = C
        self.R = R
        self.VDC = VDC
        self.CLK = CLK
        self.vout_2_cycle_ago = VDC
        self.vout_1_cycle_ago = VDC
        self.iout_1_cycle_ago = 0
    def reset(self):
        self.vout_2_cycle_ago = self.VDC
        self.vout_1_cycle_ago = self.VDC
        self.iout_1_cycle_ago = 0
    def get_curr(self, current):
        ts = 1/self.CLK
        LmulC = self.L*self.C
        LdivR = self.L/self.R
        vout = self.VDC*ts**2/(LmulC) \
            + self.vout_1_cycle_ago*(2 - ts/(LdivR)) \
            + self.vout_2_cycle_ago*(ts/(LdivR) \
            - 1 - ts**2/(LmulC)) \
            - current*self.R*ts**2/(LmulC) \
            - (1/self.C)*ts*(current - self.iout_1_cycle_ago)
            
        self.vout_2_cycle_ago = self.vout_1_cycle_ago
        self.vout_1_cycle_ago = vout
        self.iout_1_cycle_ago = current
        return vout

VDC = 1.4
pdn = PDN(
    # L = 30e-12,
    # C = 1.12e-06,
    # R = 0.0032,
    L = 30e-12,
    C = 1e-06,
    R = 0.003,
    VDC = VDC,
    CLK = 4E9,
)
power_stc = 10
power_dyn = 20
voltage = []
power = []
when_load = [0]*300 + [0.3]*300 + [1]*400 #true is load, false is no load
when_load = when_load*3

for load in when_load:
    if load:
        p = (power_stc+power_dyn*load)
    else:
        p = (power_stc)
    power.append(p) 
    voltage.append(pdn.get_curr(p/VDC))


voltage_t = []
power_t = []
throttle_start_cycles = [550] #must be always even
while throttle_start_cycles[-1] < len(when_load):
    throttle_start_cycles.append(throttle_start_cycles[-1] + 1000)


throttle_end_cycles = [] #must always even
throttle_time = 60
for i in throttle_start_cycles:
    throttle_end_cycles.append(i+throttle_time)



is_throttle = False
pdn.CLK = 4E9
pdn.reset()

i=0
while i < len(when_load):
    load = when_load[i]

    if is_throttle and load:
        p = power_dyn*when_load[i]/2 + power_stc
    elif not is_throttle and load:
        p = power_dyn*when_load[i] + power_stc
    elif is_throttle and not load or not is_throttle and not load:
        p = power_stc


    if throttle_start_cycles[0] == i:
        throttle_start_cycles.pop(0)
        is_throttle = True
        pdn.CLK = 2E9

    if throttle_end_cycles[0] == i:
        throttle_end_cycles.pop(0)
        is_throttle = False
        pdn.CLK = 4E9

    volt = pdn.get_curr(p/VDC)
    power_t.append(p)
    voltage_t.append(volt)
    if is_throttle:
        voltage_t.append(volt)
        power_t.append(p)
        i+=2
    else:
        i+=1


fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle(throttle_time, fontsize=16)
fig.set_size_inches(12.5, 7.5)

ax1.plot(range(len(voltage)), voltage, label = 'no throttle')
ax1.plot(range(len(voltage_t)), voltage_t, label = 'throttle')
ax1.legend()
ax1.set_ylim([min(min(voltage),min(voltage_t)),VDC])
ax1.set_xticks(range(0, len(voltage), 150))

# ax.set_xlim([950,1100])
ax2.plot(range(len(power)), power, label = 'no throttle')
ax2.plot(range(len(power_t)), power_t, label = 'throttle')
ax2.legend()
ax2.set_ylim([0,max(power)*1.1])


HOME = os.environ['HOME']
file_dir = HOME+ '/plot/3-31-pdn_test6.png'
plt.savefig(file_dir, dpi=300)
print(file_dir)
print('throttle min power: ', min(voltage_t))

