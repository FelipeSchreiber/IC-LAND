from tkinter import *
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import ruptures as rpt
import numpy as np

# Data for plotting
df = pd.read_csv('camera_traffic.csv')
time = list(df['Time'])
packageSize = df['Length']
bytesPerSecond = [0] *len(time)
counter = 0
for t in time:
	bytesPerSecond[int(t)] += packageSize[counter]
	counter += 1

bytesPerSecond = bytesPerSecond[0: (int(time[-1]) + 1)]
normalizedTime = list(range(0, len(bytesPerSecond)))
for i in range(len(normalizedTime)):
    bytesPerSecond[i] /= 1024
fig, ax = plt.subplots()
ax.plot(normalizedTime,bytesPerSecond)
ax.set(xlabel='time (s)', ylabel='size(bytes)',
       title='Camera traffic')
ax.grid()
fig.savefig("test2.png")
#print (int(time[-1]))
#print (len(normalizedTime))
signal = np.column_stack((normalizedTime, bytesPerSecond))
algo = rpt.Pelt(model="l2").fit(signal)
result = algo.predict(pen=90000)
rpt.display(signal,result)
plt.show()


