#https://medium.com/@j.zijlmans/lsd-slam-bc80ae01a1bb
import time, sys, os
from ros import rosbag
import roslib, rospy
roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


def CreateVideoimages(videopath, imagefolder):

    print "capuring video"
    cap = cv2.VideoCapture(videopath) #capture the videofile
    cb = CvBridge()
    # for finding cv version
    #(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    #print major_ver

    fps = cap.get(cv2.CAP_PROP_FPS) #get the fps of the videofile
    if fps != fps or fps <=1e-2:
        print "Warning: can't get fps"
    else:
        print "fps achieved succesfull: fps = "+ str(fps)
    #start a Window to show the prossesed images in
    cv2.startWindowThread()
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    print "Starting creating imgs"
    newframeavailable = True #boolean if there are new frames available
    frame_id = 0
    #loop through all the frames in the videofile
    while(newframeavailable): #as long as there are new frames availabe
        newframeavailable, frame = cap.read() #get new frame if availabe and update bool
        if not newframeavailable: #If there are now new frames
            break #stop the while loop
        #There are new frames
        frame_id += 1 #create a new frame id
        imagename = imagefolder + "/frame%d.jpg" % frame_id
        written = cv2.imwrite(imagename , frame)
        if not written:
            print "Writing frame number " + str(frame_id) + "failed"
        cv2.imshow('img',frame) #show the prossesed frame
        cv2.waitKey(1)
    #All frames have been prossesed
    print "Done creating images, closing up..."
    cv2.destroyAllWindows() #close the window
    cap.release()   #close the capture video
if len(sys.argv) == 3:

#if the user has provided enough arguments
    #extract the arguments
    videopath = sys.argv[1]
    imagefolder = sys.argv[2]
    #run the CreateVideoBag function
    CreateVideoimages(videopath, imagefolder)
    #voila
    print "Done"
else:
    #The user has not priveded the right amount of arguments, point to this
        print "Please supply two arguments as following: VideoToBag.py videopath imagefolder"
