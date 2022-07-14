import serial
import sys
import os
from datetime import datetime
import time
from subprocess import call
import pygame
from pygame.locals import *
import pygame.camera

Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
for f in os.listdir(Photo_Directory):
    os.remove(os.path.join(Photo_Directory, f))

for i in range(20):
    
    Lead_Zero_Number_Video=str(i).zfill(4)
    Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + Lead_Zero_Number_Video + ".jpg" 
    
    command='ffmpeg -f v4l2 -video_size 1920x1080 -i /dev/video0 -frames 1 '+ Name + '>/dev/null 2>&1'
    t=time.time()
    call(command,shell=True)
    print("Time to takes picture:" + str(time.time()-t))
    
    
    #ffmpeg -f video4linux2 -r 30 -s 640x480 -i /dev/video0 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi