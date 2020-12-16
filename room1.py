

import os

from mpl_toolkits import mplot3d
import sys
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

def makePoints(fileName):
        # "/home/zach/ORB_SLAM2/KeyFrameTrajectory.txt"
    print ("fileName:",fileName)

    readFile = open(fileName,"r")

    lines = readFile.readlines()
    xdata =[] 
    ydata=[] 
    print(xdata)
    zdata=[]
    for line in lines:
        vals = line.split()
        # print(vals)
        xdata.append(float(vals[1]))
        ydata.append(float(vals[2]))
        zdata.append(float(vals[3]))

    print(len(xdata),len(ydata))
    xdata = np.array(xdata) #*3.281
    zdata = np.array(zdata) #*3.281

    xdata = xdata*3.281
    zdata = zdata*3.281

    return xdata, zdata


def makeGroundTruth():

    x1 = np.linspace(0,0,1000)
    y1 = np.linspace(0,15.5,1000)  

    x2 = np.linspace(0,9.5,1000)
    y2 = np.ones(1000)*15.5


    y3 = np.linspace(15.5-9+7/12,15.5,1000)
    x3 = 9.5*np.ones(1000)

    x4 = np.linspace(6+.05/12,0,1000)
    y4 = np.zeros(1000) 

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
    return groundX,groundY


fig = plt.figure()

groundX,groundY = makeGroundTruth()
plt.scatter(groundX,groundY,label="Ground Truth")


basePath = "C:/Users/zachk/Documents/3_CMU Fall 2020/SLAM 16833/project/"
folderName = "all4 - cam1 - dynamic/"

# ORB
orb2_fileName = "KeyFrameTrajectory_JM_cam1V2_dyn_ORBSLAM2.txt"
orb2_fileName = basePath + folderName + orb2_fileName
orb2_xdata, orb2_zdata = makePoints(orb2_fileName)
plt.scatter(orb2_xdata,orb2_zdata,label='ORB-SLAM2')

dyn_fileName = "KeyFrameTrajectory_JM_cam1V2_dyn_DynaSLAM.txt"
dyn_fileName = basePath + folderName + dyn_fileName
dyn_xdata, dyn_zdata = makePoints(dyn_fileName)
plt.scatter(dyn_xdata,dyn_zdata,label='DynaSLAM')

orb3_fileName = "kf_dataset-Cam1v2_Dyn_ORBSLAM3.txt"
orb3_fileName = basePath + folderName + orb3_fileName
orb3_xdata, orb3_zdata = makePoints(orb3_fileName)
plt.scatter(orb3_xdata,orb3_zdata,label='ORB-SLAM3')


dso_fileName = "cam1v2_dyn_result_DSO.txt"
dso_fileName = basePath + folderName + dso_fileName
dso_xdata, dso_zdata = makePoints(dso_fileName)
plt.scatter(dso_xdata,dso_zdata,label='DSO')


plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.legend(loc='lower right')
plt.savefig("Room1 - Dynamic - cam1 - all4.jpg")
plt.show()