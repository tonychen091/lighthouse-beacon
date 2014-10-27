# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys

import bluetooth._bluetooth as bluez

import json

import requests
beacon_id = 1

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 30)
	print "----------"
	
	found_beacons = []
	output_array = []

	for beacon in returnedList:
		beacondata = beacon.split(",")
		uuid = beacondata[1]
		major = beacondata[2]
		minor = beacondata[3]
		rssi = beacondata[5]
		if len(uuid) == 32:
			id_string = uuid + " " + major + " " + minor
			if id_string not in found_beacons:
				print id_string
				found_beacons.append(id_string)
				beacon_item = {'uuid': uuid, 'major': major, 'minor': minor, 'rssi': rssi, 'beacon': beacon_id}
				output_array.append(beacon_item)

	
	r = requests.post("http://beacon-lighthouse-central.herokuapp.com/encounter", data=json.dumps({'encounters': output_array}, separators=(',',':')))
	print r
