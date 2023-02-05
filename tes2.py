import obd
import os

os.system("sudo rfcomm release rfcomm0")
os.system('sudo rfcomm bind rfcomm0 66:1B:11:53:71:53')

connection = obd.OBD() # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions
