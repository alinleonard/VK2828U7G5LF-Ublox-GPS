#!/usr/bin/python
import requests

server = "http://"
api = "http://api/"
payload = { 'sn': 'null', 'lat': 'null', 'lon': 'null' , 'alt': 'null', 'speed': 'null', 'utc': 'null'}
# Check server connection
def server_online(url=server, timeout=5):
    try:
        req = requests.get(url, timeout=timeout)
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print "Checking internet connection failed, status code %s" % e.response.status_code
    except requests.ConnectionError as e:
        print "No internet connection available %s" % e
    return False

def post_info(_sn, _lat, _lon):
	payload['sn'] = _sn
	payload['lat'] = _lat
	payload['lon'] = _lon

	r = requests.post(api, data=payload)
	print r.text
	if r.text == 'Accepted':
		print "sent to server"
	else:
		print "failed to send to server"
