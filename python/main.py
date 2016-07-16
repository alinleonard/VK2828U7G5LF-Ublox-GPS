#!/usr/bin/python

import os
import serial
import sys
import threading
import time
import gps_init
import gps_stream
# Serial Thread
global thread

# Serial Configuration        
ser = serial.Serial(        
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def listen_serial():
	try:
		while thread:
			bytesToRead = ser.inWaiting()
			data = ser.readline()
			gps_init.set_values(data)
	except Exception, e:
		print e
		ser.close()

if __name__ == "__main__":
	thread = True
	s = threading.Thread(name='listen_serial', target=listen_serial)
	s.start()
	try:
		while 1:
			time.sleep(5)
			gps_init.print_info()
			if gps_stream.server_online():
				gps_stream.post_info("1234",gps_init.latitude(),gps_init.longitude())
	except KeyboardInterrupt:
		thread = False
		ser.close()