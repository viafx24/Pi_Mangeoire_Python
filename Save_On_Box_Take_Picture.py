import os, time
from subprocess import Popen, PIPE, STDOUT
import pygame
from pygame.locals import *
import pygame.camera


delay_between_iteration = 0.5  # maybe useless

Global_Iteration = 0
Number_Video = 0

Number_Of_Pictures = 0
Number_Of_Images_To_Compress = 500

width = 1920
height = 1080

# initialise pygame
pygame.init()
pygame.camera.init()
# cam.stop()
cam = pygame.camera.Camera("/dev/video0", (width, height))


#Photo_Directory = "/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
prefix = "Image_"


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


cam.start()


# while Number_Of_Pictures < 5000:

for i in range(50000):
    total_time = time.time()
    #Number_Of_Pictures = len(os.listdir("/home/pi/Documents/Pictures/USB_Cam_Mangeoire")
    

    Global_Iteration = Global_Iteration + 1
    t1 = time.time()
    image = cam.get_image()
    print("Time to takes picture:" + str(time.time() - t1))
    Lead_Zero_Iteration = str(Global_Iteration).zfill(5)
    Name = "/home/pi/mnt/USB_Cam_Mangeoire/picture_" + Lead_Zero_Iteration + ".jpg"
    t2 = time.time()
    pygame.image.save(image, Name)
    print("Time to save picture:" + str(time.time() - t2))
    print("Total time:" + str(time.time() - total_time))
    print("photo number " + str(Global_Iteration) + " saved")


time.sleep(0.2)
process = Popen("sudo umount //192.168.1.1/CleMichel", shell=True)
print("Umount succesfull")


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
