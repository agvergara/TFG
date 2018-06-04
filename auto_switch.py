import subprocess
import os
import time
import socket

def check_node ( hostname, packts ):
	out_null = open(os.devnull, 'w')
	response = subprocess.call(["ping","-c",str(packts),hostname], stdout=out_null)
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

host_main_a = "193.147.53.176" 
host_main_b = "10.107.46.86" 
host_back = "10.107.46.44" 

ping_packs = 1 
flag = False # To check if the backup node is on
route_flag_main = False
route_flag_back = False

#Commands to send via UART to the waspmote: Command|IDSend|IDRecv* Command
alix_on = "alixON"
alix_off = "alixOFF"
nodes_id = "|1:4#|1:8#*"

check_main_link = 0

sleep_time = 10 # In seconds

while(True):
	host_down_a = check_node(host_main_a, ping_packs)
	host_down_b = check_node(host_main_b, ping_packs)

	if not host_down_a and not host_down_b and flag:
		check_main_link += 1
	else:
		check_main_link = 0
	
	if host_down_a or host_down_b:
		command = alix_on + nodes_id
		if not flag:
			time.sleep(1)
			send_command(command)
		flag = True
		if not route_flag_back:
			os.system("ip route replace 193.147.54.0/24 via " +  host_back)
		print "Backup link is up"
		route_flag_back = True
		route_flag_main = False
	elif flag and not host_down_a and not host_down_b:
		print "Backup link is up AND main link is up"
		print "Main link check -> " + str(check_main_link)
	else: 
		print "Main link is up"

	if flag and not host_down_a or flag and not host_down_b:
		if check_main_link >= 3:
			flag = False
			command = alix_off + nodes_id
			time.sleep(1)
			send_command(command)
			route_flag_back = False
			if not route_flag_main:
				os.system("ip route replace 193.147.54.0/24 via " + host_main_a)
			route_flag_main = True

	time.sleep(sleep_time)
