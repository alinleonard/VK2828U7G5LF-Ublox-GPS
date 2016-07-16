#!/usr/bin/python
import re

# Converts a geographic coordiante given in "degres/minutes" dddmm.mmmm
# format (ie, "12319.943281" = 123 degrees, 19.953281 minutes) to a signed
# decimal (python float) format
# # '12319.943281'
def dm_to_sd(dm):
	if not dm or dm == '0':
		return 0.
	d, m = re.match(r'^(\d+)(\d\d\.\d+)$', dm).groups()
	return float(d) + float(m) / 60



def latitude(raw):
	_lat = raw.split(',')[1]
	_dir = raw.split(',')[2]

	sd = dm_to_sd(_lat)
	if _dir == 'N':
		return +sd
	elif _dir == 'S':
		return -sd
	else:
		return 0.


def longitude(raw):
	_lon = raw.split(',')[3]
	_dir = raw.split(',')[4]
	
	sd = dm_to_sd(_lon)
	if _dir == 'E':
		return +sd
	elif _dir == 'W':
		return -sd
	else:
		return 0.

