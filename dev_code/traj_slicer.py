import os

from mpl_toolkits import mplot3d
import sys
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection='3d')


# fileName ="/home/zach/ORB_SLAM2/KeyFrameTrajectory-MH01.txt"
fileName = sys.argv[1]
# "/home/zach/ORB_SLAM2/KeyFrameTrajectory.txt"
print "fileName:",fileName

readFile = open(fileName,"r")

lines = readFile.readlines()
xdata = []
ydata=[]
zdata=[]
for line in lines:
	vals = line.split()
	# print(vals)
	xdata.append(float(vals[1]))
	ydata.append(float(vals[2]))
	zdata.append(float(vals[3]))
	ax.scatter3D(float(vals[1]),float(vals[2]),float(vals[3]))
	plt.pause(0.05)
	# exit()


# ax.scatter3D(xdata, ydata, zdata, c='r', cmap='Greens');

plt.show()
