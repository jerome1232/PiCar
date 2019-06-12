#!/usr/bin/env python3
import sys
import time
import socket
import os
import signal
import subprocess
from robot import Robot, Motor, Led_Flasher, IrSensor, ToneEmitter
GPIO.setmode(GPIO.BCM)

def signal_handler(signum, frame):
	print("Received {}. Cleaning up.".format(signum))
	GPIO.cleanup()

def main():
	###########################
	## Setting up GPIO pins ###
	###########################
	## Left Motor Pins ###
	lenable_pin = 16
	lforward_pin = 20
	lbackward_pin = 21
	## Right Motor Pins ###
	renable_pin = 13
	rforward_pin = 19
	rbackward_pin = 26
	## Motor Duty cycle and frequncy
	motorFreq = 4000
	motorDc = 100
	## IR Sensor
	ir_pin = 5  ### Maybe?
	## Blue LED
	led_pin = 12 ### Maybe?
	## Tone emitter
	spk_pin = 17 ### Maybe?
	tone = 440 ### Hertz to drive speaker at

	##################################
	# Creating left and right motors #
	##################################
	left_motor = Motor(lforward_pin, lbackward_pin, lenable_pin,
			motorDc, motorFreq)
	right_motor = Motor(rforward_pin, rbackward_pin, renable_pin,
			motorDc, motorFreq)
	##########################################
	### Creating IR sensor and LED flasher ###
	##########################################
	irSensor = IrSensor(ir_pin)
	led = Led_Flasher(led_pin)
	########################
	### Creating speaker ###
	########################
	spk = ToneEmitter(spk_pin, tone)
	#############################
	### Creating robot object ###
	#############################
	car = Robot(left_motor, right_motor, irSensor, led, spk)

	##########################################################################
	### Writting PID out to file so that PHP script can kill us on reload  ###
	##########################################################################
	pid = str(os.getpid())
	pidf_path = '/home/pi/Documents/robot_car/webpage/tmp/pid'
	try:
		os.unlink(pidf_path)
	except OSError:
		if os.path.exists(pidf_path):
			raise
	pidf = open(pidf_path, "w+")
	pidf.write(pid)
	pidf.close()
	####################################################################
	###       Creating a Unix Domain Socket for interprocess         ###
	### communication. This allows us to communicate with php script ###
	####################################################################
	server_address = '/home/pi/Documents/robot_car/webpage/tmp/pySock'
	try:
		os.unlink(server_address)
	except OSError:
		if os.path.exists(server_address):
			raise
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	print('Starting up on {}'.format(server_address))
	sock.bind(server_address)
	sock.listen(1)
	# initialising variables to False
	isW = False
	isA = False
	isD = False
	isS = False
	isQ = False
	isR = False
	isF = False
	isSpace = False
	isH = False

	# Reading from the socket to listen for data
	while not isQ:
		print('Waiting for a connection')
		conct, client_address = sock.accept()
		print('Connection from', client_address)
		data = conct.recv(64)
		data = data.decode(encoding="UTF-8", errors="strict")
		# testing the data so we can act on it
		if data:
			if data == 'wDown':
				isW = True
			elif data == 'sDown':
				isS = True
			elif data == 'spaceDown':
				isSpace = True
			elif data == 'aDown':
				isA = True
			elif data == 'dDown':
				isD = True
			elif data == 'rDown':
				isR = True
			elif data == 'fDown':
				isF = True
			elif data == 'qDown':
				isQ = True
			elif data == 'hDown':
				isH = True
			elif data == 'wUp':
				isW = False
			elif data == 'sUp':
				isS = False
			elif data == 'aUp':
				isA = False
			elif data == 'dUp':
				isD = False
			elif data == 'rUp':
				isR = False
			elif data == 'fUp':
				isF = False
			elif data == 'hUp':
				isH = False
		###
		### Begin logic to run the Car
		###
		if isW:
			car.drive("forward")
			if isA:
				car.turn("left")
			elif isD:
				car.turn("right")
		elif isS:
			car.drive("backward")
			if isA:
				car.turn("left")
			elif isD:
				car.turn("right")
		else:
			car.stop()
		if isR:
			car.changeSpeed("up")
		elif isF:
			car.changeSpeed("down")

		if isH:
			car.honk(True)
		else:
			car.honk(False)
		# Give the cpu some free time for other tasks by sleeping
		# one millisecond
		time.sleep(.01)
	# if loop has broken, stop the motor, clean pin and exit
	car.stop()
	GPIO.cleanup()

# Running main
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		GPIO.cleanup()
