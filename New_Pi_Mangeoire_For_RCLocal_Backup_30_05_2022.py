
import serial, sys, os, time
import datetime
from subprocess import Popen, PIPE, STDOUT, call, run
import smtplib



def main():
    
    # Variables
    hour_to_restart = 10
    minute_to_restart = 0

    hour_to_stop = 17
    minute_to_stop= 0

    epoch_to_restart=Compute_Hour_To_Restart(hour_to_restart,minute_to_restart)
    epoch_to_stop=Compute_Hour_To_Stop(hour_to_stop,minute_to_stop)

    Voltage_Limit_To_Shutdown_Raspi = 14.5



    Number_Of_Videos = 0
    Duration_of_Video = 30
    Frame_Per_Second = 1
    resolution='1920x1080'

    Global_Iteration = 0
    
    Open_Shared_Folder()
    Authorize_To_Write_Files()
    ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
    ser.flushInput()
    
    Initial_T = datetime.datetime.now()
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
            Data.write("Raspi start at" + str(Initial_T) + "\n" )
    
    
    while Number_Of_Videos < 5000:
        
        Number_Of_Videos=len(os.listdir("//home/pi/mnt/USB_Cam_Mangeoire"))
 
        call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi

        
        Send_String = ''       
        while Send_String.count(',')!= 6:
                b=ser.readline()
                try:
                    Send_String = b.decode()
                except:
                        pass


        try:
            
            floats = [float(x) for x in Send_String.split(",")]
            
        except:
            continue
        
        
        Transistor_State=floats[0]
        Reboot_Reason=floats[1]
        Raspi_Voltage=floats[2]
        Raspi_Current=floats[3]   
        Solar_Current=floats[4]
        Current_Epoch=floats[5]
        Epoch_Start=floats[6]
              
        Send_String= str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                     str(round(datetime.datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
                     + str(Number_Of_Videos) + ',' + str(Global_Iteration) + ','\
                     + Send_String 
        
        print(Send_String)
        
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_Ina219.txt","a")  as Data:
             Data.write(Send_String)
        
        

        if Raspi_Voltage < (Voltage_Limit_To_Shutdown_Raspi) :            
            
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("Entering the close condition due to Voltage limit measured at" + str(Raspi_Voltage) + "\n" )
            
            Send_Epoch_To_Esp32()
            print("shutdown the pi in 10 sec")
            time.sleep(10)
            print("shutdown the pi")
            run("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
            time.sleep(20)
        
        elif round(time.time()) > epoch_to_restart:
            
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("Entering the close condition due to Time limit  at" + round(time.time()) + "\n" )
            
            Send_Epoch_To_Esp32()
            
            print("shutdown the pi in 10 sec")
            time.sleep(10)
            print("shutdown the pi")
            run("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
            time.sleep(20)
                                        

        Lead_Zero_Iteration=str(Global_Iteration).zfill(5)
        video_name= "//home/pi/mnt/USB_Cam_Mangeoire/video_" + Lead_Zero_Iteration + ".mp4" 

        # compression operates in the background. Change Popen by run if want not in the background
        
        t = time.time()
        
        run([
        'ffmpeg',
        '-f', 'alsa',     #for sound      
        '-i', 'plughw:2,0', #for sound
        '-f', 'v4l2', #for video input
        '-s', resolution, 
        '-i', '/dev/video0', #the video input (USB cam
        '-t', Duration_of_Video, # time in second of video
        '-r', Frame_Per_Second, # framerate (5 would be 5fps )
        '-c:v', 'h264_omx', #raspi efficient hardware codec
        '-b:v', '8M', # level of compression 4M tp 16M should give similar result. less would decrease quality
        '-acodec', 'libmp3lame', #audio codec MP3 for efficient compression
        '-y', #erase the file if aleady exist
        video_name,           
        ],
    #    stdout=subprocess.DEVNULL,# removing output in the terminal: comment if bug to see stdout
        stderr=STDOUT,                 
        )
        
        print("Time to take video:" + str(time.time()-t))
            # testin two pass:
            #command='ffmpeg -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx -b:v 16000k -pass 1 -an -y -f mp4 /dev/null && ffmpeg -s 1920x1080 -i /dev/video0 -t 30 -r 1  -movflags +faststart -c:v h264_omx -b:v 16000k -pass 2 -y /home/pi/mnt/USB_Cam_Mangeoire/out_2_Pass.mp4'
            
            
#


def Open_Shared_Folder():
        
    process = Popen(
        "sudo mount -t cifs //192.168.1.1/CleMichel /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!",
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    
    time.sleep(0.5)# to avoid a print blanck line
    while process.poll() is None:
        print(process.stdout.readline()) 


def Compute_Hour_To_Restart(hour_to_restart,minute_to_restart):


    Date_Build=datetime.date.today() + datetime.timedelta(days=1)
    Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,  day= Date_Build.day,\
    hour = hour_to_restart,  minute= minute_to_restart, second = 0)
    epoch_to_restart= round(Wanted_Datetime.timestamp())
    
    print('Raspi will restart: ' + str(Wanted_Datetime) )
    return epoch_to_restart
    
def Compute_Hour_To_Stop(hour_to_stop, minute_to_stop):
    
    
    Date_Build=datetime.date.today()
    Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,\
    day= Date_Build.day, hour = hour_to_stop,  minute= minute_to_stop, second = 0)
    epoch_to_stop = round(Wanted_Datetime.timestamp())
    
    print("Raspi will stop: "  + str(Wanted_Datetime) )
    return epoch_to_stop


def Send_Epoch_To_Esp32():
    
    while 1:
        if ser.in_waiting:
            # it maybe needed to add some verification that the esp32 get the correct data
            Two_Epoch=str(round(time.time())) + ',' + str(epoch_to_restart ) + ','
            ser.write(Two_Epoch.encode())
            
        time.sleep(0.05)


def Authorize_To_Write_Files():

# give right to write in ina tdg if already exist and created as sudo user in rc.local
# useful when call from thonny vs from rc.local I think. but i have doubt.

    if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
        call("sudo chmod 777 /home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt", shell=True)

    if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt'):
        call("sudo chmod 777 /home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt", shell=True)



if __name__ == '__main__':
    main()



    
    



#Global_Iteration = Global_Iteration + 1
#Number_Of_Pictures = len(os.listdir("/home/pi/Documents/Pictures/USB_Cam_Mangeoire")
#command='ffmpeg -f v4l2 -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 100 -r 5 -c:v libx264 -crf 23 -preset ultrafast -vf format=yuv420p  /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2 -input_format mjpeg -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 15 -r 1 -c:v h264_omx /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 16M /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f v4l2  -input_format mjpeg  -r 20 -s 1920x1080 -i /dev/video0 -t 30 -r 20 -c:v copy  /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg  -i /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4  -c:v h264_omx  -b:v 16M  /home/pi/mnt/USB_Cam_Mangeoire/out_MJPEG_Then_OMX.mp4 -y'


#command='ffmpeg -ar 44100 -ac 1 -f alsa  -i plughw:2,0 -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec aac /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f alsa  -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'


# 
# import serial
# import sys
# import os
# from datetime import datetime
# import time
# from subprocess import call
# import subprocess 
# import pygame
# from pygame.locals import *
# import pygame.camera
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# 
# 
# time.sleep(30)
# 
# 
# call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi
# 
# delay_between_iteration=0.5 # maybe useless
# 
# Global_Iteration=0;
# Number_Video=0
# 
# Number_Of_Images_To_Compress=500;
# 
# width=1920
# height=1080
# 
# #initialise pygame
# pygame.init()
# pygame.camera.init()
# #cam.stop()
# cam = pygame.camera.Camera("/dev/video0",(width,height))
# 
# 
# Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
# prefix = "Image_"
# 
# # give right to write in ina tdg if already exist and created as sudo user in rc.local
# 
# if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
#     call("sudo chmod 777 /home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt", shell=True)
# 
# if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt'):
#     call("sudo chmod 777 /home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt", shell=True)
# 
# #remove all photos and VIDEOS in the directory before beginning
# #maybe not a good idea.
# 
# for f in os.listdir(Photo_Directory):
#     os.remove(os.path.join(Photo_Directory, f))
# 
# #ser=serial.Serial('/dev/ttyUSB0',115200, timeout=2)
# ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
# #ser=serial.Serial('/dev/ttyS0',9600, timeout=2)
# ser.flushInput()
# 
#  # test 10 seconds in case of problem. Maybe useless
#  
# cam.start()
# 
# Initial_T = datetime.now()
# 
# 
# 
# while Number_Video < 5000:
#     
#         
# 
#         Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))         
# 
#         Send_String = ''
#         
#         while Send_String.count(',')!= 12:
#                 b=ser.readline()
#                 try:
#                     Send_String = b.decode()
#                 except:
#                         pass
#    
#         try:
#             
#             floats = [float(x) for x in Send_String.split(",")]
#             
#         except:
#             continue
#             
#         Boot_Count=floats[0]
#         Reboot_Reason=floats[1]
#         Raspi_Voltage=floats[2]
#         Raspi_Current=floats[3]
#         Solar_Voltage=floats[4]     
#         Solar_Current=floats[5]
#         LDR=floats[6]
#         LDR_Average=floats[7]
#         X=floats[8]
#         Y=floats[9]
#         Z=floats[10]
#         PIR_Status=floats[11]
#         PIR_Count=floats[12]
# 
# 
#         if Reboot_Reason == 0 and Global_Iteration == 0 and os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
#              os.remove("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt")
#              
#         if   Global_Iteration == 0:   
#             try:
#                 msg = MIMEMultipart()
#                 msg['From'] = 'guillaume.baptist@gmail.com'
#                 recipients = ['guillaume.baptist@free.fr', 'guillaume.baptist@gmail.com']
#                 msg['To'] = ", ".join(recipients)
#                 msg['Subject'] = 'Raspi Start'
#                 message = 'Le raspi demarre à ' + str(Initial_T) + ' avec LDR à ' + str(LDR) + ' et voltage à ' + str(Solar_Voltage)
#                 msg.attach(MIMEText(message))
# 
#                 mailserver = smtplib.SMTP('smtp.gmail.com',587)
#                 # identify ourselves to smtp gmail client
#                 mailserver.ehlo()
#                 # secure our email with tls encryption
#                 mailserver.starttls()
#                 # re-identify ourselves as an encrypted connection
#                 mailserver.ehlo()
#                 mailserver.login('guillaume.baptist@gmail.com', 'cqfklmiaknthsvbk')
# 
#                 mailserver.sendmail('guillaume.baptist@gmail.com',recipients ,msg.as_string())
# 
#                 mailserver.quit()    
#                      
#                 print("Start Email sent")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("Start Email sent \n" )
#             
#             except:
#                 print("failed to send Email start")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("failed to send Email start \n" )
#             
#         
#         Send_String= str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
#                      str(round(datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
#                      + str(Number_Of_Pictures) + ',' + str(Global_Iteration) + ','\
#                      + Send_String 
#         
#         
#         # I have outlier with the voltage (often close to -25) and the following line are usefull to check if the voltage
#         #make sens. if not, the continue statement should allow to switch to the next iteration.
#         
#         if Solar_Voltage < 12 or Solar_Voltage > 17:
#             with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                 Data.write("outlier voltage: " + str(Solar_Voltage) + "\n")
#             continue
#         
#         
#         print(Send_String)
#         
#         with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")  as Data:
#              Data.write(Send_String)
#         
#         # this second file is never erase and thus i should check itr size regularly
#         with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#              Data.write(Send_String)
#         
# 
#         if Solar_Voltage < (14.5) or LDR > (3000) :            
#             
#             with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                  Data.write("Entering the close condition with Solar Voltage at " + str(Solar_Voltage) + " and LDR at " + str(LDR) + "\n" )
#             
#             try:   
#                 msg = MIMEMultipart()
#                 msg['From'] = 'guillaume.baptist@gmail.com'
#                 recipients = ['guillaume.baptist@free.fr', 'guillaume.baptist@gmail.com']
#                 msg['To'] = ", ".join(recipients)
#                 msg['Subject'] = 'Raspi Stop'
#                 message = 'Le raspi stoppe à ' + str(datetime.now()) + ' avec LDR à ' + str(LDR) + ' et voltage à ' + str(Solar_Voltage)
#                 msg.attach(MIMEText(message))
# 
#                 mailserver = smtplib.SMTP('smtp.gmail.com',587)
#                 # identify ourselves to smtp gmail client
#                 mailserver.ehlo()
#                 # secure our email with tls encryption
#                 mailserver.starttls()
#                 # re-identify ourselves as an encrypted connection
#                 mailserver.ehlo()
#                 mailserver.login('guillaume.baptist@gmail.com', 'cqfklmiaknthsvbk')
# 
#                 mailserver.sendmail('guillaume.baptist@gmail.com', recipients ,msg.as_string())
# 
#                 mailserver.quit()
#                 print("Email stop sent")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("Stop Email sent \n" )
#                 
#             except:
#                 print("failed to sent email stop")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("failed to sent email stop \n" )
#             
#             print("shutdown the pi in 10 sec")
#             time.sleep(10)
#             print("shutdown the pi")
#             call("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
#             time.sleep(20)
# #            call("sudo nohup shutdown -h now", shell=True)
# #
# 
#             
#         
#         t = time.time()
#         Global_Iteration=Global_Iteration + 1
#         image = cam.get_image()
#         Lead_Zero_Iteration=str(Global_Iteration).zfill(5)
#         Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + Lead_Zero_Iteration + ".jpg" 		
#         pygame.image.save(image, Name)
#         print("photo number " + str(Global_Iteration )+ " saved")
#         print("Time to takes picture:" + str(time.time()-t))      
#                   
#         ser.flushInput()
#         time.sleep(delay_between_iteration)
#         
#         
#         #print(Number_Of_Pictures % Number_Of_Images_To_Compress)
#         if Global_Iteration % Number_Of_Images_To_Compress == 0:
#                           
#             Number_Video=Number_Video + 1
# 
#             Lead_Zero_Number_Video=str(Number_Video).zfill(4)
#             Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_" + Lead_Zero_Number_Video + ".mp4" 	
#             
#             t = time.time()
#             
#             Start_Number=str(Global_Iteration - Number_Of_Images_To_Compress+1)
#             String_Number_Of_Frames=str(Number_Of_Images_To_Compress)
#             
#             print(Start_Number)
#             print(String_Number_Of_Frames)
#             
#             # compression operates in the background. Change Popen by run if want not in the background
#             subprocess.Popen([
#             'ffmpeg',
#             '-framerate', '2',
#             '-start_number', Start_Number,            
#             '-i', '/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg',
#             '-vcodec', 'libx264',
#             '-preset','ultrafast',
#             '-crf', '35',
#             '-r', '2',
#             '-frames:v', String_Number_Of_Frames,
#             Name,            
#             ],
#             stdout=subprocess.DEVNULL,# removing output in the terminal: comment if bug to see stdout
#             stderr=subprocess.STDOUT,                 
#             )
#             
# #             subprocess.Popen([
# #             'ffmpeg',
# #             '-framerate', '1',
# #             '-start_number', Start_Number,            
# #             '-i', '/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg',
# #             '-vcodec', 'mpeg4',
# #             '-qscale:v', '5',
# #             '-r', '1',
# #             '-frames:v', String_Number_Of_Frames,
# #             Name,            
# #             ],
# #             stdout=subprocess.DEVNULL,# removing output in the terminal: comment if bug to see stdout
# #             stderr=subprocess.STDOUT,                 
# #             )
#             
#              
#             #deleting images regularly
#             if Number_Of_Pictures > Number_Of_Images_To_Compress * 3:
#                 files=os.listdir(Photo_Directory)
#                 files = sorted(files)
# 
#                 for f in files[:Number_Of_Images_To_Compress]:
#                     
#                     os.remove(os.path.join(Photo_Directory, f))
#                 
#                 print(str(Number_Of_Images_To_Compress) + " photos deleted")
# 
# cam.stop()
# print("Number of video reached. end of script.")            


#ffmpeg -framerate 4 -i /home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg  -c:v mpeg4 -q:v 50 -r 4 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.avi", shell=True)
# Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))



# import serial
# import sys
# import os
# from datetime import datetime
# import time
# from subprocess import call
# import subprocess 
# import pygame
# from pygame.locals import *
# import pygame.camera
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# 
# 
# time.sleep(30)
# 
# 
# call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi
# 
# delay_between_iteration=0.5 # maybe useless
# 
# Global_Iteration=0;
# Number_Video=0
# 
# Number_Of_Images_To_Compress=500;
# 
# width=1920
# height=1080
# 
# #initialise pygame
# pygame.init()
# pygame.camera.init()
# #cam.stop()
# cam = pygame.camera.Camera("/dev/video0",(width,height))
# 
# 
# Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
# prefix = "Image_"
# 
# # give right to write in ina tdg if already exist and created as sudo user in rc.local
# 
# if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
#     call("sudo chmod 777 /home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt", shell=True)
# 
# if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt'):
#     call("sudo chmod 777 /home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt", shell=True)
# 
# #remove all photos and VIDEOS in the directory before beginning
# #maybe not a good idea.
# 
# for f in os.listdir(Photo_Directory):
#     os.remove(os.path.join(Photo_Directory, f))
# 
# #ser=serial.Serial('/dev/ttyUSB0',115200, timeout=2)
# ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
# #ser=serial.Serial('/dev/ttyS0',9600, timeout=2)
# ser.flushInput()
# 
#  # test 10 seconds in case of problem. Maybe useless
#  
# cam.start()
# 
# Initial_T = datetime.now()
# 
# 
# 
# while Number_Video < 5000:
#     
#         
# 
#         Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))         
# 
#         Send_String = ''
#         
#         while Send_String.count(',')!= 12:
#                 b=ser.readline()
#                 try:
#                     Send_String = b.decode()
#                 except:
#                         pass
#    
#         try:
#             
#             floats = [float(x) for x in Send_String.split(",")]
#             
#         except:
#             continue
#             
#         Boot_Count=floats[0]
#         Reboot_Reason=floats[1]
#         Raspi_Voltage=floats[2]
#         Raspi_Current=floats[3]
#         Solar_Voltage=floats[4]     
#         Solar_Current=floats[5]
#         LDR=floats[6]
#         LDR_Average=floats[7]
#         X=floats[8]
#         Y=floats[9]
#         Z=floats[10]
#         PIR_Status=floats[11]
#         PIR_Count=floats[12]
# 
# 
#         if Reboot_Reason == 0 and Global_Iteration == 0 and os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
#              os.remove("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt")
#              
#         if   Global_Iteration == 0:   
#             try:
#                 msg = MIMEMultipart()
#                 msg['From'] = 'guillaume.baptist@gmail.com'
#                 recipients = ['guillaume.baptist@free.fr', 'guillaume.baptist@gmail.com']
#                 msg['To'] = ", ".join(recipients)
#                 msg['Subject'] = 'Raspi Start'
#                 message = 'Le raspi demarre à ' + str(Initial_T) + ' avec LDR à ' + str(LDR) + ' et voltage à ' + str(Solar_Voltage)
#                 msg.attach(MIMEText(message))
# 
#                 mailserver = smtplib.SMTP('smtp.gmail.com',587)
#                 # identify ourselves to smtp gmail client
#                 mailserver.ehlo()
#                 # secure our email with tls encryption
#                 mailserver.starttls()
#                 # re-identify ourselves as an encrypted connection
#                 mailserver.ehlo()
#                 mailserver.login('guillaume.baptist@gmail.com', 'cqfklmiaknthsvbk')
# 
#                 mailserver.sendmail('guillaume.baptist@gmail.com',recipients ,msg.as_string())
# 
#                 mailserver.quit()    
#                      
#                 print("Start Email sent")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("Start Email sent \n" )
#             
#             except:
#                 print("failed to send Email start")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("failed to send Email start \n" )
#             
#         
#         Send_String= str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
#                      str(round(datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
#                      + str(Number_Of_Pictures) + ',' + str(Global_Iteration) + ','\
#                      + Send_String 
#         
#         
#         # I have outlier with the voltage (often close to -25) and the following line are usefull to check if the voltage
#         #make sens. if not, the continue statement should allow to switch to the next iteration.
#         
#         if Solar_Voltage < 12 or Solar_Voltage > 17:
#             with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                 Data.write("outlier voltage: " + str(Solar_Voltage) + "\n")
#             continue
#         
#         
#         print(Send_String)
#         
#         with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")  as Data:
#              Data.write(Send_String)
#         
#         # this second file is never erase and thus i should check itr size regularly
#         with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#              Data.write(Send_String)
#         
# 
#         if Solar_Voltage < (14.5) or LDR > (3000) :            
#             
#             with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                  Data.write("Entering the close condition with Solar Voltage at " + str(Solar_Voltage) + " and LDR at " + str(LDR) + "\n" )
#             
#             try:   
#                 msg = MIMEMultipart()
#                 msg['From'] = 'guillaume.baptist@gmail.com'
#                 recipients = ['guillaume.baptist@free.fr', 'guillaume.baptist@gmail.com']
#                 msg['To'] = ", ".join(recipients)
#                 msg['Subject'] = 'Raspi Stop'
#                 message = 'Le raspi stoppe à ' + str(datetime.now()) + ' avec LDR à ' + str(LDR) + ' et voltage à ' + str(Solar_Voltage)
#                 msg.attach(MIMEText(message))
# 
#                 mailserver = smtplib.SMTP('smtp.gmail.com',587)
#                 # identify ourselves to smtp gmail client
#                 mailserver.ehlo()
#                 # secure our email with tls encryption
#                 mailserver.starttls()
#                 # re-identify ourselves as an encrypted connection
#                 mailserver.ehlo()
#                 mailserver.login('guillaume.baptist@gmail.com', 'cqfklmiaknthsvbk')
# 
#                 mailserver.sendmail('guillaume.baptist@gmail.com', recipients ,msg.as_string())
# 
#                 mailserver.quit()
#                 print("Email stop sent")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("Stop Email sent \n" )
#                 
#             except:
#                 print("failed to sent email stop")
#                 with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/BackUp_Data_Ina219.txt","a")  as Data:
#                     Data.write("failed to sent email stop \n" )
#             
#             print("shutdown the pi in 10 sec")
#             time.sleep(10)
#             print("shutdown the pi")
#             call("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
#             time.sleep(20)
# #            call("sudo nohup shutdown -h now", shell=True)
# #
# 
#             
#         
#         t = time.time()
#         Global_Iteration=Global_Iteration + 1
#         image = cam.get_image()
#         Lead_Zero_Iteration=str(Global_Iteration).zfill(5)
#         Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + Lead_Zero_Iteration + ".jpg" 		
#         pygame.image.save(image, Name)
#         print("photo number " + str(Global_Iteration )+ " saved")
#         print("Time to takes picture:" + str(time.time()-t))      
#                   
#         ser.flushInput()
#         time.sleep(delay_between_iteration)
#         
#         
#         #print(Number_Of_Pictures % Number_Of_Images_To_Compress)
#         if Global_Iteration % Number_Of_Images_To_Compress == 0:
#                           
#             Number_Video=Number_Video + 1
# 
#             Lead_Zero_Number_Video=str(Number_Video).zfill(4)
#             Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/video_" + Lead_Zero_Number_Video + ".mp4" 	
#             
#             t = time.time()
#             
#             Start_Number=str(Global_Iteration - Number_Of_Images_To_Compress+1)
#             String_Number_Of_Frames=str(Number_Of_Images_To_Compress)
#             
#             print(Start_Number)
#             print(String_Number_Of_Frames)
#             
#             # compression operates in the background. Change Popen by run if want not in the background
#             subprocess.Popen([
#             'ffmpeg',
#             '-framerate', '2',
#             '-start_number', Start_Number,            
#             '-i', '/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg',
#             '-vcodec', 'libx264',
#             '-preset','ultrafast',
#             '-crf', '35',
#             '-r', '2',
#             '-frames:v', String_Number_Of_Frames,
#             Name,            
#             ],
#             stdout=subprocess.DEVNULL,# removing output in the terminal: comment if bug to see stdout
#             stderr=subprocess.STDOUT,                 
#             )
#             
# #             subprocess.Popen([
# #             'ffmpeg',
# #             '-framerate', '1',
# #             '-start_number', Start_Number,            
# #             '-i', '/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg',
# #             '-vcodec', 'mpeg4',
# #             '-qscale:v', '5',
# #             '-r', '1',
# #             '-frames:v', String_Number_Of_Frames,
# #             Name,            
# #             ],
# #             stdout=subprocess.DEVNULL,# removing output in the terminal: comment if bug to see stdout
# #             stderr=subprocess.STDOUT,                 
# #             )
#             
#              
#             #deleting images regularly
#             if Number_Of_Pictures > Number_Of_Images_To_Compress * 3:
#                 files=os.listdir(Photo_Directory)
#                 files = sorted(files)
# 
#                 for f in files[:Number_Of_Images_To_Compress]:
#                     
#                     os.remove(os.path.join(Photo_Directory, f))
#                 
#                 print(str(Number_Of_Images_To_Compress) + " photos deleted")
# 
# cam.stop()
# print("Number of video reached. end of script.")            
# 
# 
# #ffmpeg -framerate 4 -i /home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_%05d.jpg  -c:v mpeg4 -q:v 50 -r 4 /home/pi/Documents/Pictures/USB_Cam_Mangeoire/video.avi", shell=True)
# # Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))           
# #
# #