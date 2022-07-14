import serial
import sys
import os
from datetime import datetime
import time
from subprocess import call
import subprocess 
import pygame
from pygame.locals import *
import pygame.camera

call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi

delay_between_iteration=0 # maybe useless

Global_Iteration=0;
Number_Video=0

Number_Of_Images_To_Compress=100;

width=1920
height=1080

#initialise pygame
pygame.init()
pygame.camera.init()
#cam.stop()
cam = pygame.camera.Camera("/dev/video0",(width,height))


Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
prefix = "Image_"

#remove all photos and VIDEOS in the directory before beginning
#maybe not a good idea.

for f in os.listdir(Photo_Directory):
    os.remove(os.path.join(Photo_Directory, f))

#ser=serial.Serial('/dev/ttyUSB0',115200, timeout=2)
ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
#ser=serial.Serial('/dev/ttyS0',9600, timeout=2)
ser.flushInput()

time.sleep(1) # test 10 seconds in case of problem. Maybe useless
 
cam.start()

Initial_T = datetime.now() 

while Number_Video < 5000: 

        Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))         

        Send_String = ''
        
        while Send_String.count(',')!= 12:
                b=ser.readline()
                try:
                    Send_String = b.decode()
                except:
                        pass
   
        
        floats = [float(x) for x in Send_String.split(",")]
        
            
        Boot_Count=floats[0]
        Reboot_Reason=floats[1]
        Raspi_Voltage=floats[2]
        Raspi_Current=floats[3]
        Solar_Voltage=floats[4]     
        Solar_Current=floats[5]
        LDR=floats[6]
        LDR_Average=floats[7]
        X=floats[8]
        Y=floats[9]
        Z=floats[10]
        PIR_Status=floats[11]
        PIR_Count=floats[12]


        if Boot_Count == 0 and Global_Iteration == 0 and os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
             os.remove("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt")
        
        #en python, le caractère d'échappement pour descendre sur la ligne d'en dessous est "\"
        Send_String= str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                     str(round(datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
                     + str(Number_Of_Pictures) + ',' + str(Global_Iteration) + ','\
                     + Send_String 
        
        
        print(Send_String)
        
        with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")  as Data:
             Data.write(Send_String)

        if Solar_Voltage < (13.5 + 0.1) or LDR > (2000-200) :
            print("shutdown the pi in 10 sec")
            time.sleep(10)
            print("shutdown the pi")
            call("sudo nohup shutdown -h now", shell=True)
#

            
        
        t = time.time()
        Global_Iteration=Global_Iteration + 1
        image = cam.get_image()
        Lead_Zero_Iteration=str(Global_Iteration).zfill(5)
        Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + Lead_Zero_Iteration + ".jpg" 		
        pygame.image.save(image, Name)
        print("photo number " + str(Global_Iteration )+ " saved")
        print("Time to takes picture:" + str(time.time()-t))      
    
           
        ser.flushInput()
        time.sleep(delay_between_iteration)
        
        
        #print(Number_Of_Pictures % Number_Of_Images_To_Compress)
        if Global_Iteration % Number_Of_Images_To_Compress == 0:
                          
            Number_Video=Number_Video + 1

            Lead_Zero_Number_Video=str(Number_Video).zfill(4)
            Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_" + Lead_Zero_Number_Video + ".mp4" 	
            
            t = time.time()
            
            Start_Number=str(Global_Iteration - Number_Of_Images_To_Compress+1)
            String_Number_Of_Frames=str(Number_Of_Images_To_Compress)
            
            #print(Start_Number)
            #print(String_Number_Of_Frames)
            
            # compression operates in the background. Change Popen by run if want not in the background
            subprocess.Popen([
            'ffmpeg',
            '-framerate', '2',
            '-start_number', Start_Number,            
            '-i', '/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg',
            '-vcodec', 'libx264',
            '-preset','ultrafast',
            '-crf', '40',
            '-r', '2',
            '-frames:v', String_Number_Of_Frames,
            Name,            
            ],
            stdout=subprocess.DEVNULL,# removing output in the terminal: comment if bug to see stdout
            stderr=subprocess.STDOUT,                 
            )
            
             
            #deleting images regularly
            if Number_Of_Pictures > Number_Of_Images_To_Compress * 3:
                files=os.listdir(Photo_Directory)
                files = sorted(files)

                for f in files[:Number_Of_Images_To_Compress]:
                    
                    os.remove(os.path.join(Photo_Directory, f))
                
                print(str(Number_Of_Images_To_Compress) + " photos deleted")

cam.stop()
print("Number of video reached. end of script.")            


#ffmpeg -framerate 4 -i /home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg  -c:v mpeg4 -q:v 50 -r 4 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.avi", shell=True)
# Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))           
#