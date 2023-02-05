#!/usr/bin/env python3
from datetime import datetime
import time
import obd
import os
import pandas as pd
from gspread_pandas import Spread, Client
import socketio

#obd.logger.setLevel(obd.logging.DEBUG)

def get_spread():
	gc = gspread.oauth()
	worksheet = gc.open("Car Monitor")
	date = worksheet.cell( worksheet.row_count, 1 ).value
	#gas = worksheet.cell( worksheet.row_count, 3 ).value
	#send_info( str(date) + " Tay_gas: " + str(gas) )
	
def dict_to_spread( car_dict ):
	worksheet = Spread("Car Monitor")
	old_df = worksheet.sheet_to_df()
	print(old_df)
	new_df = pd.DataFrame.from_dict(car_dict, orient="index") 
	new_df = pd.concat([old_df, new_df], axis=1)
	new_df.fillna('', inplace=True)
	print(new_df)
	worksheet.df_to_sheet(new_df)
	

def bind_bt():
	os.system("sudo rfcomm release rfcomm0")
	os.system('sudo rfcomm bind rfcomm0 66:1B:11:53:71:53')

def connect_obd():
	#try: connection = obd.Async(portstr="/dev/rfcomm0",baudrate=38400, fast=True, protocol="1",timeout=10)
	try: connection = obd.OBD() # auto-connects to USB or RF port
	except: return False
		
	if connection.is_connected(): return connection
	else: return False

def car_status( connection ):
	cmd_list = connection.supported_commands
	if len(cmd_list) > 7:
		c = obd.commands.FUEL_LEVEL
		response = connection.query(c) # send the command, and parse the response
		try:
			amount = response.value.magnitude
			amount = round(amount, 2)
			gas = "Tay_gas: " + str(amount) + "%" 
			# send_info( gas )
			print(gas)
		except:
			return
			
		now = datetime.now() # current date and time
		date_date = now.strftime("%m/%d")
		date_time = now.strftime("%H:%M:%S")
		car_dict = {"DATE": date_date}
		car_dict["TIME"] = date_time
		
		for cmd in cmd_list:
			# ~ send_info(cmd.name)
			c = obd.commands[ cmd.name ] # select an OBD command (sensor)
			response = connection.query(c) # send the command, and parse the response
			#print(cmd.name, response)
			car_dict[str(cmd.name)] = [str(response)]
		
		dict_to_spread( car_dict )
	else: return
            
#worksheet = get_spread()
bind_bt()
num = 0
while True:	
	tic = time.perf_counter()
	connection = connect_obd()
	toc = time.perf_counter()
	num+=1
	if connection != False:
		car_status( connection )
		
