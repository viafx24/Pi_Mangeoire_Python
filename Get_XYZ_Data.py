import serial
ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
ser.flushInput()

while True:
	ser_bytes=ser.readline()
#	print(ser_bytes)

	Data=open("data_XYZ.txt","a")
	Data.write(ser_bytes)
