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

# Number_Of_Videos = 0
# Duration_of_Video = 15
# Frame_Per_Second = 20
# #resolution='1920x1080'
# #resolution='640x480'
# #resolution='1600x896'
# resolution='1024x768'
# Bitrate = '2M'
# Global_Iteration = 0
# 
# # 
# # 
# #Iteration_Of_Video=Get_Iteration_Of_Video() #based on iteration of the last modified file
# Lead_Zero_Iteration=str(5).zfill(5)
# video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Backup_For_Sound/video_" + Lead_Zero_Iteration + ".mp4" 
# 
# 
# t = time.time()
# print("Acquiring video...")
# 
# run([
# 'ffmpeg',
# '-f', 'alsa',     #for sound
# '-channels', '1',
# '-thread_queue_size', '4096',
# '-i', 'plughw:3,0', #for sound
# '-f', 'v4l2', #for video input
# '-s', resolution, 
# '-i', '/dev/video0', #the video input (USB cam
# '-t', str(Duration_of_Video), # time in second of video
# '-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
# '-c:v', 'h264_omx', #raspi efficient hardware codec
# '-b:v', Bitrate, # level of compression 4M tp 16M should give similar result. less would decrease quality
# #'-acodec', 'aac', #audio codec MP3 for efficient compression
# video_name,
# '-y', #erase the file if aleady exist
# ],
# # stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
# stderr=STDOUT,
# #        stderr=DEVNULL,    
# )
# 
# print("Time to take video:" + str(time.time()-t))
# 
# 
Number_Of_Videos = 0
Duration_of_Video = 120
Frame_Per_Second = 5
#resolution='1920x1080'
resolution='640x480'
resolution_2='1600x896'
#resolution='1024x768'
Bitrate = '2M'
Global_Iteration = 0

Lead_Zero_Iteration=str(1).zfill(5)
video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4" 

Lead_Zero_Iteration=str(2).zfill(5)
video_name_2= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4" 


t = time.time()
print("Acquiring video...")

run([
'ffmpeg',
'-f', 'alsa',     #for sound
'-channels', '1',
'-thread_queue_size', '4096',
'-i', 'plughw:2,0', #for sound


'-f', 'alsa',     #for sound
'-channels', '1',
'-thread_queue_size', '4096',
'-i', 'plughw:3,0', #for sound


#'-thread_queue_size', '4096',
'-f', 'v4l2', #for video input

#'-input_format', 'mjpeg',

#'-use_wallclock_as_timestamps', '1',
'-i', '/dev/video0', #the video input (USB cam
'-s', resolution,
#'-thread_queue_size', '4096',


'-i', '/dev/video2', #the video input (USB cam
'-s', resolution_2,
'-t', str(Duration_of_Video), # time in second of video
'-r', str(Frame_Per_Second), # framerate (5 would be 5fps )

#'-c:v', 'copy', #raspi efficient hardware codec
#'-vf', 'setpts=PTS-STARTPTS',
#'-vsync', '0',
'-c:v', 'h264_omx', #raspi efficient hardware codec
'-b:v', Bitrate,
#'-filter_complex', 'hstack=inputs=2',
# level of compression 4M tp 16M should give similar result. less would decrease quality
#'-acodec', 'aac', #audio codec MP3 for efficient compression
'-map','0',
'-map','2',
video_name,

'-t', str(Duration_of_Video), # time in second of video
'-r', str(Frame_Per_Second), # framerate (5 would be 5fps )

#'-c:v', 'copy', #raspi efficient hardware codec
#'-vf', 'setpts=PTS-STARTPTS',
#'-vsync', '0',
'-c:v', 'h264_omx', #raspi efficient hardware codec
'-b:v', Bitrate,
'-map','1',
'-map','3',
video_name_2,


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