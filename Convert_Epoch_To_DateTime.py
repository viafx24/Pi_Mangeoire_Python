import serial, sys, os, time
import datetime

Send_String= str(datetime.datetime.fromtimestamp(1655639902).strftime("%d/%m/%Y %H:%M:%S"))

print(Send_String)