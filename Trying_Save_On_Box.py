import os, time
from subprocess import Popen, PIPE, STDOUT

# Note: Try with shell=True should not be used, but it increases readability to new users
process = Popen('sudo mount -t cifs //192.168.1.1/Raspi /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!', shell=True, stdout=PIPE, stderr=PIPE)

while process.poll() is None:
    print(process.stdout.readline()) # For debugging purposes, 

print(os.listdir('/home/pi/mnt'))

time.sleep(2)
process = Popen('sudo umount //192.168.1.1/Raspi', shell=True)


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