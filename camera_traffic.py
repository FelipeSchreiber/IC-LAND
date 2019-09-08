#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# Data for plotting
datasets = ['./2018-6-26/net.if.out(eth0.2).csv','./2018-6-25/net.if.out(eth0.2).csv','./2018-6-22/net.if.out(eth0.2).csv']
count = 0
for dataset in datasets:
	df = pd.read_csv(dataset)
	df = df.loc[df.mac == 'B0-4E-26-F9-C6-54']
	df['mac'].unique()
	

	# In[16]:


	timestamp = list(df['timestamp'])
	bytesPerSecond = list(df['value'])
	#len(timestamp)


	# In[12]:


	fig, ax = plt.subplots()
	fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(18.5, 10.5)
	#fig.savefig('test2png.png', dpi=100)
	ax.plot(timestamp,bytesPerSecond)
	ax.set(xlabel='time (s)', ylabel='size(bytes)',
		     title='Camera traffic')
	ax.grid()
	fig.savefig("camera_traffic.png")


	exec(open("detect_cumsum.py").read())
	ta, tai, taf, amp = detect_cusum(bytesPerSecond, threshold=np.mean(bytesPerSecond), drift=np.std(bytesPerSecond)/5, ending=True, show=True, ax=None)
	plt.clf()
	plt.cla()
	fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(18.5, 10.5)
	x = [timestamp[i] for i in ta] 
	y = [bytesPerSecond[i] for i in ta]
	plt.scatter(x, y, s=50,color='red')
	plt.plot(timestamp,bytesPerSecond)
	plt.show()
	fig.savefig(str(count)+"_cusum_changepoints.png")
	count += 1

