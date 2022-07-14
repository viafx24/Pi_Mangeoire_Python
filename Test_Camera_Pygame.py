#!/usr/bin/python
import os
#import pygame, sys
import time
# from pygame.locals import *
# import pygame.camera
from subprocess import call
#import serial


# width = 720
# height = 576#480


width=1920
height=1080

#initialise pygame
# pygame.init()
# pygame.camera.init()
# cam = pygame.camera.Camera("/dev/video0",(width,height))
#cam.start()

#setup window
#windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
#pygame.display.set_caption('Camera')

#ser=serial.Serial('/dev/ttyUSB0',9600, timeout=2)
#ser.flushInput()

iteration=0

#cam.start()
t = time.time()

# Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture"
# 
# call(['fswebcam','-q','-b','-l','1','-r','1920x1080','--no-banner','--save','/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%Y-%m-%d_%H:%M:%S.jpg'])
# 
# time.sleep(15) 
# 
# call(['sudo','pkill','fswebcam'])

# 
# 
# 
# 
t = time.time()
for iteration in range(4):
    #image = cam.get_image()
    Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + str(iteration + 1)+ ".jpg"
    #time.sleep(0.1)
    call(['fswebcam','-q','-r','1920x1080','--no-banner',Name])
    #pygame.image.save(image, Name)
    #.sleep(0.1) 

#     call(['fswebcam','-q','-r','1920x1080','--no-banner',Name])
#     
#     #			time.sleep(2)	
#                 #display the picture
#     catSurfaceObj = image
#     windowSurfaceObj.blit(catSurfaceObj,(0,0))
#     pygame.display.update()
#     Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + str(iteration + 1)+ ".jpg" 		
#    pygame.image.save(windowSurfaceObj,Name)
#   time.sleep(0.05)

elapsed = time.time() - t
#cam.stop()


print(elapsed)
# 
# 
# 
# 
# 
# 
# 
# while True:
# 	ser.flushInput()
# 	ser_bytes=ser.readline()
# #	print(ser_bytes[0])
# #	time.sleep(0.51)
# 	if ser_bytes[0]=="Q":
# 		iteration=iteration + 1
# 		print(iteration)
# 		if iteration > 250:
# 			break
# #		print("souris!")
# #		time.sleep(1)
# 		cam.start()
# 		for iteration_2 in range(10):
# 			image = cam.get_image()
# #			time.sleep(2)	
# 			#display the picture
# 			catSurfaceObj = image
# 			windowSurfaceObj.blit(catSurfaceObj,(0,0))
# 			pygame.display.update()
# 			Name= "/home/pi/A_image/Detection_" + str(iteration) + "_picture_" + str(iteration_2 + 1)+ ".jpg" 		
# 			pygame.image.save(windowSurfaceObj,Name)
# 			time.sleep(0.05)
# 		cam.stop()
# 		
# print("number of iteration exceeded")		