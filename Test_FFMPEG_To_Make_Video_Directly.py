import serial
import sys
import os
from datetime import datetime
import time
from subprocess import call, STDOUT, DEVNULL
import pygame
from pygame.locals import *
import pygame.camera

# Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
# for f in os.listdir(Photo_Directory):
#     os.remove(os.path.join(Photo_Directory, f))

for i in range(1):
    
#     Lead_Zero_Number_Video=str(i).zfill(4)
#     Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + Lead_Zero_Number_Video + ".jpg" 
#     
#     command='ffmpeg -f v4l2 -video_size 1920x1080 -i /dev/video0 -frames 1 '+ Name + '>/dev/null 2>&1'
    
# -vcodec libx264 -preset ultrafast -crf 25 
#    command='ffmpeg -t 30  -r 0.5 -s 1920x1080 -i /dev/video0 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
#    command='ffmpeg -s 1920x1080 -i /dev/video0 -frames 30 -r 1  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
#    command='ffmpeg -s 1920x1080  -f v4l2 -pix_fmt mjpeg -framerate 5 -i /dev/video0 -frames 30 -r 1  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
#    command='ffmpeg -f v4l2 -input_format mjpeg -i /dev/video0 -frames 30 -r 1 -vcodec libx264 -preset ultrafast -crf 35 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
#    command='ffmpeg -f v4l2 -input_format mjpeg -s 1920x1080 -i /dev/video0 -frames 30 -r 1 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
#    command='ffmpeg -s 1920x1080 -i /dev/video0 -t 30  -r 2  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
    
#    command='ffmpeg -s 1920x1080 -i /dev/video0 -t 30  -r 2 -vcodec libx264 -crf 25 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'

    #command='ffmpeg -f v4l2 -input_format mjpeg -r 1  -s 1920x1080 -i /dev/video0 -t 30 -r 1 -vcodec libx264 -crf 25 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
    #command='ffmpeg -f v4l2  -r 2  -s 1920x1080 -i /dev/video0 -t 30 -r 2  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
    #command='ffmpeg -f v4l2 -r 10 -input_format mjpeg -i /dev/video0 -t 10 -c:v copy /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.mkv -y'
    command='ffmpeg -f v4l2 -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 100 -r 1 -c:v libx264 -crf 25 -preset veryfast -vf format=yuv420p  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.mp4 -y'
    
    

    
    
    #command='ffmpeg -f v4l2 -r 5 -video_size 1920x1080  -i /dev/video0 -t 20 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
  #    command='ffmpeg -f v4l2 -input_format mjpeg -s 1920x1080 -i /dev/video0 -frames 10 -r 1  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
#    command='ffmpeg -s 1920x1080 -i /dev/video0 -frames 30 -r 1  /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.mp4 -y'
#    command='ffmpeg -f v4l2 -r 5 -video_size 1920x1080 -input_format mjpeg -i /dev/video0 -frames 15 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.mkv -y'
#    command='ffmpeg -t 30  -s 1920x1080 -i /dev/video0 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi -y'
    #command='ffmpeg -f v4l2 -framerate 1 -video_size 1920x1080  -input_format mjpeg -i /dev/video0 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.mkv
#    command='ffmpeg -f v4l2 -framerate 1 -video_size 1280x720 -input_format mjpeg -i /dev/video0 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.mkv'
#    command='ffmpeg -t 30 -framerate 1 -video_size 1920x1080 -i /dev/video0 -c copy /home/pi/Documents/Pictures/USB_Cam_Mangeoire/mjpeg.mkv'
    t=time.time()
    call(command,shell=True)
    print("Time to takes picture:" + str(time.time()-t))
    
    
    #ffmpeg -f video4linux2 -r 30 -s 640x480 -i /dev/video0 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/out.avi