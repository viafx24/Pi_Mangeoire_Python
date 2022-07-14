
import serial
import sys
import os
from datetime import datetime
import time
from subprocess import call
import pygame
from pygame.locals import *
import pygame.camera



if os.path.isfile('/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.mp4'):
    os.remove("/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.mp4")
    

if os.path.isfile('/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_2.mp4'):
    os.remove("/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_2.mp4")
    

t = time.time()
#call("ffmpeg -framerate 0.5  -i /home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg -c:v libx264 -r 2 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.mp4", shell=True)

call("ffmpeg -framerate 2  -i /home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg -c:v libx264 -preset ultrafast  -crf 35 -r 2 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.mp4", shell=True)

print("Time to takes picture:" + str(time.time()-t))
print(os.path.getsize('/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.mp4'))

t = time.time()

call("ffmpeg -framerate 2  -i /home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg -c:v libx264 -preset ultrafast  -crf 25 -r 2 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_2.mp4", shell=True)

print("Time to takes picture:" + str(time.time()-t))
print(os.path.getsize('/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_2.mp4'))