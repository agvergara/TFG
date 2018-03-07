import os
import time
import socket

def check_node ( hostname, packts ):
	response = os.system("ping -c " + str(packts) + " " + hostname + " > /dev/null")
	return response

def send_command ( command ):
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/webcom")
    try:
    	s.send(command)
    except:
    	print("Command " + command + " not sent to Waspmote")
    s.close()
	print "Command sent to Waspmote! -> " + command

host_main = "google.es" # IP of the main node
host_back = "193.147.53.170" # IP of the backup node
ping_packs = 1 # Packets of the ping to check if the nodes are up
flag = False # To check if the backup node is on

#Commands to send via UART to the waspmote: Command|IDSend|IDRecv* Command
alix_on = "ALIXON"
alix_off = "ALIXOFF"
nodes_id = "|1:4#|1:8#*"

sleep_time = 120 # In seconds

while(True):
	host_down = check_node(host_main, ping_packs)

	if host_down:
		flag = True
		command = alix_on + nodes_id
		send_command(command)
	
	if flag and not host_down:
		flag = False
		command = alix_on + nodes_id
		send_command(command)

	time.sleep(sleep_time)