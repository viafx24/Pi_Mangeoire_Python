import glob
import serial, sys, os, time
import datetime
from subprocess import Popen, PIPE, STDOUT, DEVNULL, call, run
import smtplib
from math import nan



def main():
    
    
    call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi
    Open_Shared_Folder()# to write video on the internet box
    Authorize_To_Write_Files()

#     # Variables
#     
#     ABSOLUTE_STOP = True
#     ABSOLUTE_START = True
#      
# #     ABSOLUTE_STOP = False
# #     ABSOLUTE_START = False
#     
#     day_to_stop = 0
#     hour_to_stop = 21
#     minute_to_stop = 0
#     
#     day_to_restart = 1
#     hour_to_restart = 18
#     minute_to_restart = 0
#     
#     epoch_to_stop=Compute_Hour_To_Stop(hour_to_stop,minute_to_stop,day_to_stop,ABSOLUTE_STOP)
#     epoch_to_restart=Compute_Hour_To_Restart(hour_to_restart,minute_to_restart,day_to_restart,ABSOLUTE_START)
    


    Number_Of_Videos = 0
    Duration_of_Video = 60
    Frame_Per_Second = 5
    # resolution='1920x1080'
    # resolution_2='1600x896'
    # resolution='640x480'
    # resolution='1024x768'
    resolution='1600x896'
    Bitrate = '2M'
# Bitrate_2 = '1M'
    Global_Iteration = 0
    
    
    
    Initial_T = datetime.datetime.now()
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write("Program launch at " + str(Initial_T) + "\n" )
            
    # specific log file of a raspi session (remove it each time raspi boot)
            
    
    while Number_Of_Videos < 5000:
        
        Global_Iteration = Global_Iteration + 1 
        
        time.sleep(0.1)
        Number_Of_Videos=len(os.listdir("//home/pi/mnt/USB_Cam_Mangeoire/Video"))
        time.sleep(0.1)
        
        Iteration_Of_Video=Get_Iteration_Of_Video() #based on iteration of the last modified file
        print(Iteration_Of_Video)
        Lead_Zero_Iteration=str(Iteration_Of_Video).zfill(5)
        video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4"
        print(video_name)
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
            Data.write("Beginning " + video_name + " at " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\n" ) 
        

        
        t = time.time()
        print("Acquiring video...")
        
# Change run by Popenif want that ffmpeg works in the background

        run([
        'ffmpeg',
        '-f', 'alsa',     #for sound
        '-channels', '1',
        '-thread_queue_size', '1024',
        '-i', 'plughw:2,0', #for sound

        '-f', 'v4l2', #for video input
#        '-thread_queue_size', '4096',
        '-s', resolution,
        '-i', '/dev/video0', #the video input (USB cam)
        
        '-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
        '-t', str(Duration_of_Video), # time in second of video
        '-c:v', 'h264_omx', #raspi efficient hardware codec
        '-b:v', Bitrate, # the lowest, the highest compression but more bad quality
        video_name,
        '-y', #erase the file if aleady exist
        ],
        stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
        stderr=STDOUT,
        #        stderr=DEVNULL,    
        )
        
        print("Time to take video:" + str(time.time()-t))

# create /home/pi/mnt with the path of internet box         
def Open_Shared_Folder():
        
    process = Popen(
        "sudo mount -t cifs //192.168.1.1/CleMichel /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!",
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    
    time.sleep(1)# to avoid a print blanck line
    # code present on internet example to trow error if failed, i think
    while process.poll() is None:
        print(process.stdout.readline()) 

# allow to define a time to restart in absolute or relative way
def Compute_Hour_To_Restart(hour_to_restart,minute_to_restart,day_to_restart,ABSOLUTE_START):
      
    if ABSOLUTE_START == True :
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_restart)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,  day= Date_Build.day,\
        hour = hour_to_restart,  minute= minute_to_restart, second = 0)
           
        
    elif ABSOLUTE_START == False:
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_restart,hours=hour_to_restart,\
        minutes=minute_to_restart)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,  day= Date_Build.day,\
        hour = Date_Build.hour,  minute= Date_Build.minute, second = 0)
    
    
    epoch_to_restart= round(Wanted_Datetime.timestamp())
    print('Raspi will restart: ' + str(Wanted_Datetime) )
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write('Raspi will restart: ' + str(Wanted_Datetime) + "\n" )
    
    return epoch_to_restart


# allow to define a time to stop in absolute or relative way
def Compute_Hour_To_Stop(hour_to_stop, minute_to_stop,day_to_stop,ABSOLUTE_STOP):
    
    if ABSOLUTE_STOP == True :
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_stop)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,\
        day= Date_Build.day, hour = hour_to_stop,  minute= minute_to_stop, second = 0)
        
    elif  ABSOLUTE_STOP == False :
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_stop,hours=hour_to_stop,\
        minutes=minute_to_stop)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,\
        day= Date_Build.day, hour = Date_Build.hour,  minute= Date_Build.minute , second = 0)
        
    epoch_to_stop = round(Wanted_Datetime.timestamp())
    
    print("Raspi will stop: "  + str(Wanted_Datetime) )
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write('Raspi will stop: ' + str(Wanted_Datetime) + "\n" )
    
    return epoch_to_stop

# usefull to detect the last modified file and use its name to found the next iteration 
# that shoudl be used.

def Get_Iteration_Of_Video():


    list_of_files = glob.glob('//home/pi/mnt/USB_Cam_Mangeoire/Video/*') # * means all if need specific format then *.csv


    if  len(list_of_files) > 0    : 
        latest_file = max(list_of_files, key=os.path.getctime)
        Iteration_Of_Last_Video = int(latest_file[-9:-4])
        Iteration_Of_Video = Iteration_Of_Last_Video + 1
        print(Iteration_Of_Video)
          
    else :
        Iteration_Of_Video = 1
        print(Iteration_Of_Video)

    return Iteration_Of_Video

# serial communication between esp32 and raspi are not always easy. This script
# send a message to the esp32 to tell it what time is it and when the transistor should
# be turn on again to switch on again the raspi. Since errors and bugs occurs, it is needed
# to check that the esp32 had received the epochs and send back aknowledgement. A double
# aknowledgement is also used for debugging purpose but probably became useless. the major
# part of this code is for debugging purpose and may probably be simplified. 

def Send_Epoch_To_Esp32(ser,epoch_to_restart):
        
    i = 0
    j = 0
    # the difficutly was to wait that esp32 awake from light sleep.
    ser.reset_input_buffer()
    while 1:
               
        if ser.in_waiting: #to avoid to do the ser.write during light sleep.
            
            Line=ser.readline().decode()

            # will try to send the two epochs untils the answer from esp32 is "Epoch received"
            while Line != "Epoch received\r\n":
                i = i+1
                Two_Epoch= "Epoch Sent," + str(round(time.time())) + ',' + str(epoch_to_restart ) + ','
                
                print(Two_Epoch)
                ser.write(Two_Epoch.encode())
                print("Break Sent:" + str(i))
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                      Data.write("Break Sent:" + str(i) + "\n")
                #time.sleep(8) #critical
                
                ser.reset_input_buffer()
                t = time.time()     
                while  ser.in_waiting < 1:
                        time.sleep(0.25)
                        
                
                print("Time in the while loop:" + str(time.time()-t))
                time.sleep(0.25) 
                Line=ser.readline().decode()
                print(Line)
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                      Data.write(Line + "\n")
               
                ser.write("Double check OK".encode())
                
            break
        time.sleep(0.25)
        j=j+1
        print("j= " + str(j))
        # with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        #               Data.write("j= " + str(j) + "\n")

#  rc.local launch the script as root (i may change this behaviour in the future). 
# there is complicated consequencies and when calling the script from thonny, i think, it's
# better to give all right to files to avoid errors (based on my memory unperfect)

def Authorize_To_Write_Files():



    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt'):

        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt", shell=True)

    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Log.txt'):
    
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Log.txt", shell=True)
        
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt'):
        
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt", shell=True)
        
        
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt'):
        
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt", shell=True)

# the complex serial communication to receive all data of the night (raspi off) from esp32
# when raspi boot. This function generates less bug that the one with the epoch.

def Received_All_Transistor_Off_Data_from_ESP32(ser):
        
    i = 0

    while 1:

        if ser.in_waiting:
            
            
            if i == 1:
                Line=ser.readline().decode()
                ser.write("Raspi Ready sent".encode())
                print("Raspi Ready sent")
                
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("Raspi Ready sent" + "\n" )
                
                time.sleep(2) # soudl be rather 10 ?
            
            
            i = i+1

            if i == 2:
                Line=ser.readline().decode()
                if Line == "ESP32 Ready received\r\n":
                    print("ESP32 Ready received")
                    
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("ESP32 Ready received" + "\n" )
                    
                    time.sleep(2)

            
            else:
                
                Send_String=ser.readline().decode()
                
                if Send_String == "End of transmission\r\n":
                    print("End of transmission")
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("End of transmission" + "\n" )
                    
                    break
                
                else:

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
                    
                    Send_String= str(datetime.datetime.fromtimestamp(Current_Epoch).strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                    str(float(nan)) + ','\
                    + str(float(nan)) + ',' + str(float(nan)) + ','\
                    + Send_String 
            
                    print(Send_String)
                    
                        
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt","a")  as Data:
                        Data.write(Send_String)
        
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt","a")  as Data:
                         Data.write(Send_String)
                        

                                   
               
        time.sleep(0.005)

# pythonic way to allow to put function below the main script.

if __name__ == '__main__':
    main()



  
#command='ffmpeg -f v4l2 -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 100 -r 5 -c:v libx264 -crf 23 -preset ultrafast -vf format=yuv420p  /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2 -input_format mjpeg -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 15 -r 1 -c:v h264_omx /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 16M /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f v4l2  -input_format mjpeg  -r 20 -s 1920x1080 -i /dev/video0 -t 30 -r 20 -c:v copy  /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg  -i /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4  -c:v h264_omx  -b:v 16M  /home/pi/mnt/USB_Cam_Mangeoire/out_MJPEG_Then_OMX.mp4 -y'
#command='ffmpeg -ar 44100 -ac 1 -f alsa  -i plughw:2,0 -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec aac /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f alsa  -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'

