#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Decription: Test PiCAN 2 Interface
Version: 4/2018 Roboball (MattK.)
"""
import can 
import os
import time
from collections import deque

#### init can bus globals ####
freq = 0.5 # set receiver frequency, e.g. 0.5
num_sens = 2 # number of sensor data 
cells = 6 # number of cells per battery pack (accus)
# init buffer
a1_V_list = [] # accu 1 voltage
a1_T_list = [] # accu 1 temperature
a2_V_list = [] # accu 2 voltage
a2_T_list = [] # accu 2 temperature
for cell in range(cells):
	a1_V_list.append(deque(maxlen=20))
	a1_T_list.append(deque(maxlen=20))
	a2_V_list.append(deque(maxlen=20))
	a2_T_list.append(deque(maxlen=20))
print(a1_V_list[0])

#### Bring up the can0 Interface ####
# Close can0 if still open
os.system("sudo /sbin/ip link set can0 down")
# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)	
# Connect to can0 interface 
bus = can.interface.Bus(channel='can0', bustype='socketcan_native') 
print('connected to can0 interface')
print('ready to send/receive can messages')

def filter_buffer(byte_list, msg_id):
	''' a filter for CAN messages to sort into diff. buffer'''
	byte2 = byte_list[1] + byte_list[2]
	#print(byte2)
	# convert from hex to dec
	val_dec = int(byte2, 16) / 100
	print(val_dec)
	
	# filter into buffer (temperature and voltages)
	for pos2 in range(1,num_sens+1):
		for pos3 in range(1,cells+1):
			if byte_list[0] == str(pos2) + str(pos3):
				print('sorting byte '+ str(pos2) + str(pos3) + '!!')
				# sort for ID: 600 (Accu 1)
				if msg_id == 600:
					# sort for temperatures
					if pos2 == 1:
						#print(a1_T_list[pos3-1])
						a1_T_list[pos3-1].append(val_dec)
						#print(a1_T_list[pos3-1])
					# sort for voltages
					if pos2 == 2:
						#print(a1_V_list[pos3-1])
						a1_V_list[pos3-1].append(val_dec)
						#print(a1_V_list[pos3-1])		
				# sort for ID: 602 (Accu 2)
				if msg_id == 602:
					# sort for temperatures
					if pos2 == 1:
						#print(a2_T_list[pos3-1])
						a2_T_list[pos3-1].append(val_dec)
						#print(a2_T_list[pos3-1])
					# sort for voltages
					if pos2 == 2:
						print(a2_V_list[pos3-1])
						a2_V_list[pos3-1].append(val_dec)
						print(a2_V_list[pos3-1])

if __name__ == '__main__':
	while (True):
		#print(list(a1_V_list[0]))
		# receive CAN messages
		msg = bus.recv()
		len_msg = len(msg.data)
		#print(vars(msg))
		#print(msg)
		#print(msg.arbitration_id) # 1536= ID 600, 1537= ID 601 (Error Akku1), 
		msg_id = int('{0:x} '.format(msg.arbitration_id))
		#print(msg_id)
		#print(msg.timestamp)
		#print(msg.data)
		# check correct msg length	
		if len_msg == 3:
			byte_list = [] # init empty bytestring
			for pos in range(len_msg-1,-1,-1):
				byte = '{0:x}'.format(msg.data[pos])
				print(byte) 
				if len(byte) == 1:
					byte = '0' + byte
					#print(byte)
					#print('Length ',len(byte))
				byte_list.append(byte)
				#print(pos)
			print(byte_list)
			# call filtering for values
			filter_buffer(byte_list, msg_id)
		# update frequency					
		time.sleep(freq)
