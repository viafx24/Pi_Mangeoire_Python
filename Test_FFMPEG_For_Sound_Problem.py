#import serial
import sys
import os
import time
from subprocess import run, STDOUT, DEVNULL, call



video_name="//home/pi/mnt/USB_Cam_Mangeoire/Video/2_Test_Sound.mp4"
Duration_of_Video = 10
Frame_Per_Second = 1
resolution='1920x1080'



t = time.time()
print("Acquiring video...")

# command='ffmpeg -f alsa -i plughw:2,0 -t 10 -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
# call(command,shell=True)
#command='ffmpeg -f alsa -channels 2 -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 10 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f alsa -channels 1 -i plughw:2,0 -f v4l2  -s 1024x576 -i /dev/video0 -t 10 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M_LOW.mp4 -y'
#command='ffmpeg -f alsa -channels 1 -i plughw:2,0 -f v4l2  -s 1280x720 -i /dev/video0 -t 10 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M_MEDIUM.mp4 -y'
#command='ffmpeg -f alsa -channels 1 -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 10 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M_HIGH.mp4 -y'
command='ffmpeg -f alsa   -i plughw:2,0 -f v4l2  -s 1920x1080   -i /dev/video0 -t 10 -r 1 -c:v h264_omx  -b:v 8M  -c:a aac -b:a 128k /home/pi/mnt/USB_Cam_Mangeoire/out_16M_MEDIUM_HIGH.mp4 -y'
#command='ffmpeg -f alsa  -i plughw:2,0 -f v4l2  -input_format yuyv422 -s 1920x1080 -i /dev/video0 -t 10 -r 1 -c:v libx264 -preset ultrafast -crf 40  /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
call(command,shell=True)
# 
# run([
# 'ffmpeg',
# '-f', 'alsa',     #for sound      
# '-i', 'plughw:2,0', #for sound
# '-f', 'v4l2', #for video input
# '-s', resolution, 
# '-i', '/dev/video0', #the video input (USB cam
# '-t', str(Duration_of_Video), # time in second of video
# '-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
# '-c:v', 'h264_omx', #raspi efficient hardware codec
# '-b:v', '8M', # level of compression 4M tp 16M should give similar result. less would decrease quality
# #'-acodec', 'libmp3lame', #audio codec MP3 for efficient compression
# video_name,
# '-y', #erase the file if aleady exist
# ],
# #        stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
# stderr=STDOUT,
# #        stderr=DEVNULL,    
# )

print("Time to take video:" + str(time.time()-t))

