import glob
import os, time
import smtplib
from subprocess import Popen, PIPE, STDOUT, DEVNULL, call, run

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

list_of_files = glob.glob('//home/pi/mnt/USB_Cam_Mangeoire/Test/*') # * means all if need specific format then *.csv


if  len(list_of_files) > 0    : 
    latest_file = max(list_of_files, key=os.path.getctime)
    Iteration_Of_Last_Video = int(latest_file[-9:-4])
    Iteration_Of_Video = Iteration_Of_Last_Video + 1
    print(Iteration_Of_Video)
      
else :
    Iteration_Of_Video = 1
    print(Iteration_Of_Video)

      