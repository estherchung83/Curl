#!/usr/bin/python

#library to parse user input
import argparse

#library for regex to do string matching
import re

#library for socket for http request/response process
from socket import *

#creates a argparse object to be able to parse through command line
parser = argparse.ArgumentParser()

#specifies that it expects 0 or more arguments
parser.add_argument("user_commands", nargs = '*')

args = parser.parse_args()

requested_url = ' '.join([str(item) for item in args.user_commands])

#used to see if user inputted a server name or ip address
ipAdr_present = False
hostname_present = False
ipAdr_present1 = False
hostname_present1 = False

#to intialize variables
dst_port = None
server_ip = None
server_hostname = None
html_object = None

#checks the number of user entered commands. Only accepts 1-2 arguments
if(len(args.user_commands) == 0):
	print("Invalid command. Must specify at least 1 argument. Rerun program and try again")
	exit()
elif(len(args.user_commands) > 2):
	print("Invalid command. Program only supports 2 arguments. Rerun program and try again")
	exit()

#user specified 1 argument
elif(len(args.user_commands) == 1):

	#check if url contains https
	if(re.search("^https", args.user_commands[0])):
		print("https is not supported. Only supports http. Rerun program and try again")
		exit()

	#determines if user inputted an host name or ip address
	if(re.search("^http://[0-9]",args.user_commands[0])):
		ipAdr_present = True
	elif((re.search("^http://[a-z,A-z]",args.user_commands[0]))):
		hostname_present = True

	#parse for destination port
	dst_present = re.findall(":[0-9]+", args.user_commands[0])

	#user specifed a destination port
	if len(dst_present) == 1:
		dst_port = dst_present[0][1:]
		no_dstport = False
	else:
		dst_port = 80
		no_dstport = True

	user_split = re.findall("/[a-zA-Z0-9.:]*", args.user_commands[0])
	user_split2 = re.findall("/[a-zA-Z0-9.]*", args.user_commands[0])

	#there might be html objects
	if len(user_split) > 2:
		#check if its just slash at end of url and no html object
		if user_split[2] == "/":

			if ipAdr_present == True:
				server_ip = user_split2[1][1:]

			if hostname_present == True:
				server_hostname = user_split2[1][1:]
				og_hostname = user_split2[1][1:] + "/"

			html_object = None

		#there is html objects
		else:
			if ipAdr_present == True:
				server_ip = user_split2[1][1:]

			if hostname_present == True:
				server_hostname = user_split2[1][1:]
				og_hostname = user_split2[1][1:]

			html_object = ""
			for obj in user_split[2:]:
				html_object += obj

	#no html object
	else:
		if ipAdr_present == True:
			server_ip = user_split2[1][1:]

		if hostname_present == True:
			server_hostname = user_split2[1][1:]
			og_hostname = user_split2[1][1:]

		html_object = None

	#no ip address, find ip address using server host name
	if ipAdr_present == False:
		server_ip = gethostbyname(server_hostname)

#user specifed 2 arguments
else:
	#check if url contains https
	if(re.search("^https", args.user_commands[0]) or re.search("^https", args.user_commands[1])):
		print("https is not supported. Only supports http. Rerun program and try again")
		exit()

	#parse for destination port in first argument
	dst_present = re.findall(":[0-9]+", args.user_commands[0])

	#user specifed a destination port
	if len(dst_present) == 1:
		dst_port = dst_present[0][1:]
		no_dstport = False
	else:
		dst_port = 80
		no_dstport = True

	#determines if user inputted an host name or ip address in first argument
	if(re.search("^http://[0-9]",args.user_commands[0])):
		ipAdr_present = True
	elif((re.search("^http://[a-z,A-z]",args.user_commands[0]))):
		hostname_present = True

	#determines if user inputted an host name or ip address in 2nd argument
	if(re.search("^http://[0-9]",args.user_commands[1])):
		ipAdr_present1 = True
	elif((re.search("^http://[a-z,A-z]",args.user_commands[1]))):
		hostname_present1 = True

	#determine if second argument is server 
	user_split = re.findall("/[a-zA-Z0-9.]*", args.user_commands[0])

	#there may be html object in first argument
	if len(user_split) > 2:
		#check if its just slash at end of url and no html object
		if user_split[2] == "/":

			if ipAdr_present == True:
				server_ip = user_split[1][1:]

			if hostname_present == True:
				server_hostname = user_split[1][1:]
				og_hostname = user_split[1][1:] + "/"

			html_object = None
		#there is html objects
		else:
			if ipAdr_present == True:
				server_ip = user_split[1][1:]

			if hostname_present == True:
				server_hostname = user_split[1][1:]
				og_hostname = user_split[1][1:]

			html_object = ""
			for obj in user_split[2:]:
				html_object += obj
	#no html object
	else:
		if ipAdr_present == True:
			server_ip = user_split[1][1:]

		if hostname_present == True:
			server_hostname = user_split[1][1:]
			og_hostname = user_split[1][1:]

		html_object = None

	#checks 2nd arguments
	#make sure not overwriting the user given destination port
	if dst_port is not None:
		#parse for destination port in first argument
		dst_present = re.findall(":[0-9]+", args.user_commands[0])

		#user specifed a destination port
		if len(dst_present) == 1:
			dst_port = dst_present[0][1:]
			no_dstport = False
		else:
			dst_port = 80
			no_dstport = True

	# help parse 2nd command ine argument
	user_split = re.findall("[a-zA-Z0-9.]*", args.user_commands[1])

	#make sure not overwriting the user given server hostname
	if server_hostname is None:
		#checks if url ends if a slash
		temp = re.findall("/$", args.user_commands[1])
		
		#there is a slash at end of url
		if len(temp) == 1:
			server_hostname = user_split[0]
			og_hostname = user_split[0] + "/"
		else:
			server_hostname = user_split[0]
			og_hostname = user_split[0]
	else:
		pass

	#make sure not overwriting the user given server ip address
	if server_ip is None:
		server_ip = user_split[0]
	else:
		pass

	#make sure not overwriting the user given HTML object
	if html_object is None:
		user_split = re.findall("/[a-zA-Z0-9.]*", args.user_commands[1])
		print(user_split)

		# no html object, just part of url
		if user_split[0] == "/":
			html_object = None
		else:
			html_object = ""
			for obj in user_split:
				html_object += obj

	#no ip address, find ip address using server host name
	if ipAdr_present == False:
		server_ip = gethostbyname(server_hostname) 

#creates socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#create socket timeout 
clientSocket.settimeout(6)

#establish TCP connection
clientSocket.connect((server_ip, int(dst_port)))

#create GET request
if html_object is not None:
	getRequest = "GET " + html_object + " HTTP/1.1\r\n" + "Host: " + server_hostname + "\r\n\r\n"
else:
	getRequest = "GET "+ "/" + " HTTP/1.1\r\n" + "Host: " + server_hostname + "\r\n\r\n"

#gets source ip and source port
getSourceInfo = clientSocket.getsockname()
source_ip = getSourceInfo[0]
source_port = getSourceInfo[1]

#sends GET request to server
clientSocket.send(getRequest.encode())

try:
	#receives http response from server
	modifiedSentence = clientSocket.recv(4096)
except Exception as e:
	#close socket
	clientSocket.close()

	#print to terminal
	print("TCP Error: Empty reply from server, " + requested_url + ", " + str(e))

	#log into Log.csv
	#append to Log.csv
	file = open("Log.csv","a")
	file.write("Unsuccessful, " + ", " + requested_url + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + str(e) +  "\n")
	file.close()

	exit()

#decode from bytes to string
response = modifiedSentence.decode()

#separating http header from data
temp = re.split("\r\n\r\n", response)

#holds http header
http_response = temp[0]

#get http status line
temp1 = re.split("\r\n", http_response)
status_line = temp1[0]

#get status code
temp2 = re.split(" ", status_line)
status_code = temp2[1]

#get content length
temp3 = re.findall("Content-Length: [0-9]*",http_response)

#there is content length in header
if len(temp3) > 0:
	content_length = int(temp3[0][16:])
else:
	content_length = 0

#get any data in intial receive
data_start = re.search("\r\n\r\n",response)
data = response[data_start.start()+4:]

# checks for chunk encoding
chunked = re.search("Transfer-Encoding: chunked", http_response)

#There is chunk encoding 
if chunked is not None:

	#write to HTMLoutput.html
	file = open("HTTPoutput.html","w")
	file.write(data)

	#calculates the intial bytes left to read
	bytes_left_read = content_length - len(data)

	#loops untill all bytes have been read
	while bytes_left_read >= 0:
		 receive = clientSocket.recv(4096)
		 file.write(receive.decode())

		 #update the amount of bytes left to read
		 bytes_left_read = bytes_left_read - 4096

		 #close file after reading to it
	file.close()

	print("Chunk encoding is not supported")

	#log into csv file
	file = open("Log.csv","a")
	file.write("Unsuccessful, " + status_line + ", " + args.user_commands[0] + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + status_line + "\n")
	file.close()

	clientSocket.close()
	exit()

yes_success = re.search("^HTTP/1.1 2", status_line)

no_success_4xx = re.search("^HTTP/1.1 4", status_line)

#checks for success http status line
if yes_success is not None:

	#write to HTMLoutput.html
	file = open("HTTPoutput.html","w")
	file.write(data)

	#calculates the intial bytes left to read
	bytes_left_read = content_length - len(data)

	#loops untill all bytes have been read
	while bytes_left_read >= 0:
		 receive = clientSocket.recv(4096)
		 file.write(receive.decode())

		 #update the amount of bytes left to read
		 bytes_left_read = bytes_left_read - 4096

		 #close file after reading to it
	file.close()

	#print to terminal
	print("Success, " + requested_url + ", " + status_line)

	#append an entry in log.csv
	file = open("Log.csv", "a")
	file.write("Successful, " + status_code + ", " + requested_url + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + status_line + "\n")
	file.close()

elif no_success_4xx is not None:
	#write to HTMLoutput.html
	file = open("HTTPoutput.html","w")
	file.write(data)

	#calculates the intial bytes left to read
	bytes_left_read = content_length - len(data)

	#loops untill all bytes have been read
	while bytes_left_read > 0:
		try:
			receive = clientSocket.recv(4096)
		except Exception as e:
			#close connection to server
			clientSocket.close()

			#print to terminal
			print("Unsuccessful, " + requested_url + ", " + status_line)

			#append to Log.csv
			file = open("Log.csv","a")
			file.write("Unsuccessful, " + status_code + ", " + requested_url + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + status_line + "\n")
			file.close()

			exit()

		file.write(receive.decode())

		 #update the amount of bytes left to read
		bytes_left_read = bytes_left_read - 4096

	#close file after reading to it
	file.close()

	#print to terminal
	print("Unsuccessful, " + requested_url + ", " + status_line)

	#append to Log.csv
	file = open("Log.csv","a")
	file.write("Unsuccessful, " + status_code + ", " + requested_url + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + status_line + "\n")
	file.close()

#unsuccessful 
else:
	#write to HTMLoutput.html
	file = open("HTTPoutput.html","w")
	file.write(data)

	#calculates the intial bytes left to read
	bytes_left_read = content_length - len(data)

	#loops untill all bytes have been read
	while bytes_left_read > 0:
		try:
			receive = clientSocket.recv(4096)
		except Exception as e:
			#close connection to server
			clientSocket.close()

			#print to terminal
			print("Unsuccessful, " + requested_url + ", " + status_line)

			#append to Log.csv
			file = open("Log.csv","a")
			file.write("Unsuccessful, " + status_code + ", " + requested_url + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + status_line + "\n")
			file.close()

			exit()

		file.write(receive.decode())

		 #update the amount of bytes left to read
		bytes_left_read = bytes_left_read - 4096

	#close file after reading to it
	file.close()
	
	#print to terminal
	print("Unsuccessful, " + requested_url + ", " + status_line)

	#append to Log.csv
	file = open("Log.csv","a")
	file.write("Unsuccessful, " + status_code + ", " + requested_url + ", " + og_hostname + ", " + str(source_ip) + ", " + str(server_ip) + ", " + str(source_port) + ", " + str(dst_port) + ", " + status_line + "\n")
	file.close()

#close connection to server
clientSocket.close()


