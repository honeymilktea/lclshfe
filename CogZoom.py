import pandas as pd
import matplotlib.pyplot as plt
from numpy import mean
import math

df = pd.read_excel('Sys_Stability.xlsx', header=None, index_col=None, usecols="A")
system_stability = df[0]
time_duration = len(system_stability)
cognitive_zoom = [1] * time_duration
cognitive_zoom_2 = [1] * time_duration
weight = [1/5, 1/4, 1/3, 1/2, 1]
midpoint = time_duration/2  # midpoint of the anxious curve
scale = 0.07    # slope of the anxious curve
# system status: stability (Sys_S), transparency (Sys_T; known vs. unknown required time for troubleshooting)
# known troubleshooting time    + time is short -> high attention?
# known troubleshooting time    + time is long  -> off task
# unknown troubleshooting time  + time is short ->
# unknown troubleshooting time  + time is long  ->
# operator status: fatigue (Op_F), anxiety (Op_A; time need to complete tasks + data value + time left), experience (Op_E; in instrument and in type of experiment)
# Attention[t] = 1/Sys_S[t-5:5] + 1/Op_F[t] + Op_A[t] ? Op_E ? Sys_T

for i in range(time_duration):
    if i <= 5:
        cognitive_zoom[i] = min((100/mean(system_stability[0:i])) + 1/(1 + math.exp((-i + midpoint) * scale)), 3)
        cognitive_zoom_2[i] = min((100/mean(system_stability[0:i])) + 1/(1 + math.exp((-i + midpoint) * scale)), 3)
    else:
        cognitive_zoom[i] = min(100/mean(system_stability[i-5:i]) + 1/(1 + math.exp((-i + midpoint) * scale)), 3)
        cognitive_zoom_2[i] = min(100/(system_stability[i-5:i].mul(weight).div(sum(weight)).sum()) + 1/(1 + math.exp((-i + midpoint) * scale)), 3)

fig, axs = plt.subplots(3, sharex=True)
axs[0].plot(system_stability)
axs[0].set_title('System Stability')
axs[0].set_ylabel('Stability')
axs[1].plot(cognitive_zoom)
axs[1].set_ylabel('by Average')
axs[1].set_title('Attentiveness')
# axs[1].set_xlabel('Time')
axs[2].plot(cognitive_zoom_2)
axs[2].set_ylabel('by 1/x')
# axs[2].set_title('Cognitive Zoom')
axs[2].set_xlabel('Time')
plt.show()
