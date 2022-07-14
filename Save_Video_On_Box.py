import os, time
from subprocess import Popen, PIPE, STDOUT, call


Global_Iteration = 0
Number_Video = 0

width = 1920
height = 1080




# Note: Try with shell=True should not be used, but it increases readability to new users
process = Popen(
    "sudo mount -t cifs //192.168.1.1/CleMichel /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!",
    shell=True,
    stdout=PIPE,
    stderr=PIPE,
)

while process.poll() is None:
    print(process.stdout.readline())  # For debugging purposes,

print(os.listdir("/home/pi/mnt"))


# while Number_Of_Pictures < 5000:

for i in range(1):
    
    #Number_Of_Pictures = len(os.listdir("/home/pi/Documents/Pictures/USB_Cam_Mangeoire")
    #command='ffmpeg -f v4l2 -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 100 -r 5 -c:v libx264 -crf 23 -preset ultrafast -vf format=yuv420p  /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
    #command='ffmpeg -f v4l2 -input_format mjpeg -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 15 -r 1 -c:v h264_omx /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
    #command='ffmpeg -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 16M /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
    #command='ffmpeg -f v4l2  -input_format mjpeg  -r 20 -s 1920x1080 -i /dev/video0 -t 30 -r 20 -c:v copy  /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
    #command='ffmpeg  -i /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4  -c:v h264_omx  -b:v 16M  /home/pi/mnt/USB_Cam_Mangeoire/out_MJPEG_Then_OMX.mp4 -y'
    
    
    #command='ffmpeg -ar 44100 -ac 1 -f alsa  -i plughw:2,0 -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec aac /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
    command='ffmpeg -f alsa  -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
    
    
    # testin two pass:
    #command='ffmpeg -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx -b:v 16000k -pass 1 -an -y -f mp4 /dev/null && ffmpeg -s 1920x1080 -i /dev/video0 -t 30 -r 1  -movflags +faststart -c:v h264_omx -b:v 16000k -pass 2 -y /home/pi/mnt/USB_Cam_Mangeoire/out_2_Pass.mp4'
    
    
    t = time.time()
    call(command,shell=True)
    print("Time to takes picture:" + str(time.time()-t))

#     Global_Iteration = Global_Iteration + 1
#     t1 = time.time()
#     image = cam.get_image()
#     print("Time to takes picture:" + str(time.time() - t1))
#     Lead_Zero_Iteration = str(Global_Iteration).zfill(5)
#     Name = "/home/pi/mnt/USB_Cam_Mangeoire/picture_" + Lead_Zero_Iteration + ".jpg"
#     t2 = time.time()
#     pygame.image.save(image, Name)
#     print("Time to save picture:" + str(time.time() - t2))
#     print("Total time:" + str(time.time() - total_time))
#     print("photo number " + str(Global_Iteration) + " saved")


# time.sleep(0.2)
# process = Popen("sudo umount //192.168.1.1/CleMichel", shell=True)
# print("Umount succesfull")


#
# import time
# import serial
# import os
#
#
# ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
# ser.flushInput()
#
#
# for i in range(20):
#   time.sleep(0.5)
#   if i % 2 ==0:
#       print("I send 1")
#       ser.write(b"1")
#   else:
#       print("I send 0")
#       ser.write(b"0")
#
#
#   ser_bytes=ser.readline()
#   Bytes_2_String=str(ser_bytes)
#   Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
#   print(Pretty_Line)
#
#
# ser.close() # close serial port to allow uploading sketches
# print("The Serial Port is closed")
#
#
#


# import os
# from subprocess import Popen, PIPE, STDOUT
#
# # Note: Try with shell=True should not be used, but it increases readability to new users
# process = Popen('sudo mount -t cifs //192.168.1.1/Raspi ~/mnt -o vers=1.0,username=pi,password=cardyna!', shell=True,)
# while process.poll() is None:
#     print(process.stdout.readline()) # For debugging purposes, in case it asks for password or anything.
#
# print(os.listdir('/home/pi/mnt'))
#
# process = Popen('sudo umount //192.168.1.1/Raspi', shell=True)
