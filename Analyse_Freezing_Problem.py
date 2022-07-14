import glob
import serial, sys, os, time
import datetime
from subprocess import Popen, PIPE, STDOUT, DEVNULL, call, run
import smtplib
from math import nan

def Open_Shared_Folder():
        
    process = Popen(
        "sudo mount -t cifs //192.168.1.1/CleMichel /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!",
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    
    time.sleep(1)# to avoid a print blanck line
    while process.poll() is None:
        print(process.stdout.readline()) 


Open_Shared_Folder()

Duration_of_Video = 10
Frame_Per_Second = 5
#resolution='1920x1080'
#esolution='640x480'
resolution='1600x896'
#resolution='1024x768'
Bitrate = '2M'
Global_Iteration = 0

Lead_Zero_Iteration=str(4).zfill(5)
video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Test/video_" + Lead_Zero_Iteration + ".mp4" 

# Lead_Zero_Iteration=str(2).zfill(5)
# video_name_2= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4" 


t = time.time()
print("Acquiring video...")

        
run([
'ffmpeg',
'-f', 'alsa',     #for sound
'-channels', '1',
'-thread_queue_size', '4096',
'-i', 'plughw:2,0', #for sound
'-f', 'v4l2', #for video input
#'-thread_queue_size', '4096',
'-s', resolution,
'-i', '/dev/video0', #the video input (USB cam

#'-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
'-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
'-t', str(Duration_of_Video), # time in second of video
'-c:v', 'h264_omx', #raspi efficient hardware codec
'-b:v', Bitrate,
video_name,
'-y', #erase the file if aleady exist
],
stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
stderr=STDOUT,
#        stderr=DEVNULL,    
)

print("Time to take video:" + str(time.time()-t))

# Duration_of_Video = 15
# 
# Lead_Zero_Iteration=str(12).zfill(5)
# video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Backup_For_Sound/Sound_" + Lead_Zero_Iteration + ".wav" 
# 
# 
# t = time.time()
# print("Acquiring video...")
# 
# run([
# 'ffmpeg',
# '-f', 'alsa',     #for sound
# '-channels', '1',
# '-i', 'plughw:2,0', #for sound
# #'-acodec', 'aac', #audio codec MP3 for efficient compression
# '-t', str(Duration_of_Video),
# video_name,
# '-y', #erase the file if aleady exist
# ],
# #stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
# stderr=STDOUT,
# #        stderr=DEVNULL,    
# )
# 
# print("Time to take video:" + str(time.time()-t))
# 
# Lead_Zero_Iteration=str(11).zfill(5)
# video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Backup_For_Sound/Sound_" + Lead_Zero_Iteration + ".wav" 
# 
# 
# t = time.time()
# print("Acquiring video...")
# 
# run([
# 'ffmpeg',
# '-f', 'alsa',     #for sound
# '-channels', '1',
# '-i', 'plughw:3,0', #for sound
# #'-acodec', 'aac', #audio codec MP3 for efficient compression
# '-t', str(Duration_of_Video),
# video_name,
# '-y', #erase the file if aleady exist
# ],
# #stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
# stderr=STDOUT,
# #        stderr=DEVNULL,    
# )
# 
# print("Time to take video:" + str(time.time()-t))