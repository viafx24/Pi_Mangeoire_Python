import os

Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"


files=os.listdir(Photo_Directory)
files = sorted(files)

for f in files[:10]:
    print(f)
    os.remove(os.path.join(Photo_Directory, f))
