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


# 
Number_Of_Videos = 0
Duration_of_Video = 60
Frame_Per_Second = 1
#resolution='1920x1080'
#resolution='640x480'
#resolution='1600x896'
resolution='1024x768'
Bitrate = '1M'
Global_Iteration = 0

# Lead_Zero_Iteration=str(14).zfill(5)
# video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Backup_For_Sound/video_" + Lead_Zero_Iteration + ".mp4" 


Lead_Zero_Iteration=str(1).zfill(5)
video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4"
print(video_name)
Lead_Zero_Iteration=str(2).zfill(5)
video_name_2= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4" 
print(video_name_2)


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

# run([
#  'ffmpeg',
# # '-f', 'alsa',     #for sound
# # '-channels', '1',
# # '-t', str(Duration_of_Video), # time in second of video
# # '-thread_queue_size', '4096',
# # '-i', 'plughw:2,0', #for sound
# 
# 
# # '-f', 'alsa',     #for sound
# # '-channels', '1',
# # '-t', str(Duration_of_Video), # time in second of video
# # '-thread_queue_size', '4096',
# # '-i', 'plughw:3,0', #for sound
# 
# 
# '-thread_queue_size', '4096',
# 
# '-f', 'v4l2', #for video input
# 
# '-t', str(Duration_of_Video), # time in second of video
# '-s', '640x480',
# '-r', str(15), # framerate (5 would be 5fps )
# 
# '-i', '/dev/video2', #the video input (USB cam
# #       '-thread_queue_size', '4096',
# 
# '-t', str(Duration_of_Video), # time in second of video
# #'-s', '1920x1080',
# #'-s', '1024x576',
# '-s', '640x480',
# '-r', str(5), # framerate (5 would be 5fps )
# 
# '-thread_queue_size', '4096',
# '-i', '/dev/video0', #the video input (USB cam       
# '-c:v', 'h264_omx', #raspi efficient hardware codec
# '-b:v', '0.5M',
# #       '-filter_complex', 'hstack=inputs=2',
# # level of compression 4M tp 16M should give similar result. less would decrease quality
# #'-acodec', 'aac', #audio codec MP3 for efficient compression
# #'-map', '0',
# '-map', '0',
# video_name,
# 
# '-c:v', 'h264_omx', #raspi efficient hardware codec
# '-b:v', '0.5M',
# '-map', '1',
# #'-map', '2',
# video_name_2,
# '-y', #erase the file if aleady exist
# ],
# #stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
# #stderr=STDOUT,
# #        stderr=DEVNULL,    
# )



# run([
# 'ffmpeg',
# '-f', 'alsa',     #for sound
# '-channels', '1',
# '-thread_queue_size', '4096',
# '-i', 'plughw:2,0', #for sound
# #'-thread_queue_size', '4096',
# '-f', 'v4l2', #for video input
# '-s', resolution,
# '-input_format', 'mjpeg',
# 
# #'-use_wallclock_as_timestamps', '1',
# '-i', '/dev/video0', #the video input (USB cam
# #'-thread_queue_size', '4096',
# #'-i', '/dev/video2', #the video input (USB cam
# '-t', str(Duration_of_Video), # time in second of video
# '-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
# 
# '-c:v', 'copy', #raspi efficient hardware codec
# #'-vf', 'setpts=PTS-STARTPTS',
# #'-vsync', '0',
# #'-c:v', 'h264_omx', #raspi efficient hardware codec
# #'-b:v', Bitrate,
# #'-filter_complex', 'hstack=inputs=2',
# # level of compression 4M tp 16M should give similar result. less would decrease quality
# #'-acodec', 'aac', #audio codec MP3 for efficient compression
# video_name,
# '-y', #erase the file if aleady exist
# ],
# #stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
# #stderr=STDOUT,
# #        stderr=DEVNULL,    
# )

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