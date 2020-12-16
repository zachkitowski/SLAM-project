import os

from mpl_toolkits import mplot3d
import sys
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
# ax = plt.axes(projection='3d')
# "C:/Users/zachk/Documents/3_CMU Fall 2020/SLAM 16833/project/cam1V2/KeyFrameTrajectory_JM_cam1V2_static_ORBSLAM2.txt"
# KeyFrameTrajectory_JM_cam1V2_static_ORBSLAM2
# fileName ="/home/zach/ORB_SLAM2/KeyFrameTrajectory-MH01.txt"
# fileName = sys.argv[1]
fileName = "C:/Users/zachk/Documents/3_CMU Fall 2020/SLAM 16833/project/cam1V2/KeyFrameTrajectory_JM_cam1V2_static_ORBSLAM2.txt"

# "/home/zach/ORB_SLAM2/KeyFrameTrajectory.txt"
print ("fileName:",fileName)

readFile = open(fileName,"r")

lines = readFile.readlines()
xdata =[] #np.empty(dtype=float)#[]
ydata=[] #np.empty(dtype=float)
print(xdata)
zdata=[]
for line in lines:
	vals = line.split()
	# print(vals)
	xdata.append(float(vals[1]))
	ydata.append(float(vals[2]))
	zdata.append(float(vals[3]))
	# ax.scatter3D(float(vals[1]),float(vals[2]),float(vals[3]))
	# ax.scatter(float(vals[1]),float(vals[2]))
	# plt.pause(0.05)
	# exit()

print(len(xdata),len(ydata))
xdata = np.array(xdata) #*3.281
zdata = np.array(zdata) #*3.281

xdata = xdata*3.281
zdata = zdata*3.281

plt.scatter(xdata,zdata)

x1 = np.linspace(0,0,1000)
y1 = np.linspace(0,15.5,1000)  

# x1 = x1/3.281
# y1 = y1/3.281



# plt.scatter(x1,y1)

x2 = np.linspace(0,9.5,1000)
y2 = np.ones(1000)*15.5
# print(y2)
# x2 = x2/3.281
# y2 = y2/3.281

# plt.scatter(x2,y2)


y3 = np.linspace(15.5-9+7/12,15.5,1000)
x3 = 9.5*np.ones(1000)
# x3 = x3/3.281
# y3 = y3/3.281

# plt.scatter(x3,y3)

x4 = np.linspace(6+.05/12,0,1000)
y4 = np.zeros(1000) 

# x4 = x4/3.281
# y4 = y4/3.281

# plt.scatter(x4,y4)



x5 = np.linspace(9.5,6+.05/12,1000)
y5 = np.linspace(15.5-9+7/12,0,1000)

groundX = np.concatenate((x1,x2))
groundX = np.concatenate((groundX,x3))
groundX = np.concatenate((groundX,x4))
groundX = np.concatenate((groundX,x5))


groundY = np.concatenate((y1,y2))
groundY = np.concatenate((groundY,y3))
groundY = np.concatenate((groundY,y4))
groundY = np.concatenate((groundY,y5))


groundX = groundX/ 3.281
groundY = groundY/ 3.281

plt.scatter(groundX,groundY)
plt.show()
