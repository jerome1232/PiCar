#!/usr/bin/env python3
import socket
import sys
import os

def main():
	server_address = '/home/pi/Documents/robot_car/webpage/tmp/pySock'
	pid = os.getpid()
	pid = str(pid)
	pidf_path= '/home/pi/Documents/robot_car/webpage/tmp/pid'
	try:
		os.unlink(pidf_path)
	except OSError:
		if os.path.exists(pidf_path):
			raise
	pidf = open(pidf_path, "w+")
	pidf.write(pid)
	pidf.close()

	try:
		os.unlink(server_address)
	except OSError:
		if os.path.exists(server_address):
			raise
	count = 1
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	print('starting up on {}'.format(server_address))
	sock.bind(server_address)
	sock.listen(1)

	while True:
		print('Waiting for a connection')
		connection, client_address = sock.accept()
		print('connection from', client_address)
		data = connection.recv(64)
		data = data.decode(encoding="utf-8", errors="strict")
		if data:
			print('received', data)
			if (data == '81'):
				print("Q was pressed")
				sys.exit()

	if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
