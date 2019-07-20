#!/usr/bin/env python3
import sys
import time
import socket
import os
import signal
import RPi.GPIO as GPIO
import subprocess
from robot import Robot, Motor, Led_Flasher, IrSensor, ToneEmitter


def signal_handler(signum, frame):
	""" Cleans up gpio pins and temporary files on interupt. """

	print("Received {}. Cleaning up.".format(signum))
	GPIO.cleanup()

def main():
	###########################
	## Setting up GPIO pins ###
	###########################
	## Left Motor Pins ###
	# enable, forward, reverse
	lMotorPins = [16, 20, 21]
	## Right Motor Pins ###
	# enable, forward, reverse
	rMotorPins = [13, 19, 26]
	## Motor Duty cycle and frequncy
	# frequency, duty cycle
	motorPwm = [4000, 100]
	## IR Sensor
	ir_pin = 6
	## Blue LED
	led_pin = 12
	## Tone emitter
	# pin, hertz
	spk_pin = [17, 440]
	## Setting up I2C for battery voltage monitor
	i2c = busio.I2C(board.SCL, board.SDA)
	ads = ADS.ADS1115(i2c)
	chan = AnalogIn(ads, ADS.P1)

	##################################
	# Creating left and right motors #
	##################################
	# left_motor = Motor(lforward_pin, lbackward_pin, lenable_pin,
	# 		motorDc, motorFreq)
	# right_motor = Motor(rforward_pin, rbackward_pin, renable_pin,
	# 		motorDc, motorFreq)
	##########################################
	### Creating IR sensor and LED flasher ###
	##########################################
	# irSensor = IrSensor(ir_pin)
	# led = Led_Flasher(led_pin)
	# ########################
	# ### Creating speaker ###
	# ########################
	# spk = ToneEmitter(spk_pin, tone)
	#############################
	### Creating robot object ###
	#############################
	car = Robot(lMotorPins, rMotorPins, ir_pin, ledPin, spk_pin)
	##########################################################################
	### Writting PID out to file so that PHP script can kill us on reload  ###
	##########################################################################
	pid = str(os.getpid())
	pidf_path = 'tmp/pid'
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
		###
		### Begin logic to run the Car
		###
	while (result == robot.getInput()):
		if data == 'isW':
			car.drive("forward")
			if data == 'isA':
				car.turn("left")
			elif data =='isD':
				car.turn("right")
		elif data == 'isS':
			car.drive("backward")
			if data == 'isA':
				car.turn("left")
			elif data == 'isD':
				car.turn("right")
		else:
			car.stop()
		if data == 'isR':
			car.changeSpeed("up")
		elif data == 'isF':
			car.changeSpeed("down")

		if data == 'isH':
			car.honk(True)
		else:
			car.honk(False)
		# Give the cpu some free time for other tasks by sleeping
		# one millisecond
		time.sleep(.1)
	# if loop has broken, stop the motor, clean pin and exit
	car.stop()
	GPIO.cleanup()
	os.unlink(server_address)

# Running main
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		GPIO.cleanup()
