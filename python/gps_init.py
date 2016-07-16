import gps_protocol_nmea
import os

_data = '' # Serial values
_fix = False # Gps fix
_lat = 0
_lon = 0
_satN = 0 # Sat number

# call this every time new reading on serial
def set_values(data):
	global _data
	_data = data
	fix() # SET GPS FIX
	set_position() # SET GPS POSITION
	set_sat_number() # SET SAT NUMBER

# PRIVATE

def fix():
	global _fix
	if _data.startswith("$GPGLL"):
		if _data.split(',')[6] == "A":
			_fix = True
		else:
			_fix = False

def set_position():
	global _lat, _lon
	if _data.startswith("$GPGLL"):
		_lat = gps_protocol_nmea.latitude(_data)
		_lon = gps_protocol_nmea.longitude(_data)

def set_sat_number():
	global _satN
	if _data.startswith("$GPGGA"):
		_satN = _data.split(',')[7]

# PUBLIC

def is_fix():
	if _fix:
		return True
	else:
		return False

def latitude():
	return _lat

def longitude():
	return _lon

def sat_number():
	return _satN

def print_info():
	os.system('clear')
	print _data
	if is_fix():
		print
		print ' GPS reading'
		print '----------------------------------------'
		print 'latitude    ' , latitude()
		print 'longitude   ' , longitude()
		# print 'time utc    ' , utc
		# print 'altitude (m)' , gpsd.fix.altitude
		# print 'eps         ' , gpsd.fix.eps
		# print 'epx         ' , gpsd.fix.epx
		# print 'epv         ' , gpsd.fix.epv
		# print 'ept         ' , gpsd.fix.ept
		# print 'speed (km/h) ' , speed
		print
		print 'sats        ' , sat_number()
	else:
		print
		print "NO GPS LOCK"
		print
