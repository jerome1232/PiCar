#!/usr/bin/env python3
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

###################################
### Class defines entire robot. ###
###################################
class Robot:
	"""
	Create a robotic car with two motors, an ir sensor and a speaker.

	Attributes:
		rightMotor : (motor)
			Motor on right side of the car.
		leftMotor : (motor)
			Motor on the left side of the car.
		motorDc : (int)
			Dutycycle to run motors at.
		motorFreq : (int)
			Number of times per second to pulse signal to motors.
		irSensor : (irSensor)
			Check if an object is behind car.
		led : (Led_Flasher)
			Turns on/off a flashing LED.
		spk : (ToneEmitter)
			Object to emit sound, primarily used as a horn.

	Methods:
		drive(direction)
			Drives both motors forwards or backwards.

		turn(direction)
			Turns the car right or left, reversed while backup up.

		stop()
			Stops both motors.

		changeSpeed(upDown)
			Changes motor duty cycle up or down to speed up or slow down
			both motors.

		honk(doHonk)
			Honks the horn!
	"""

	def __init__(self, rightMotor, leftMotor, irSensor, led, spk):
		""""
		Attributes:
			rightMotor : (motor)
				The motor/motors on right side.
			leftMotor : (motor)
				The motor/motrs on left side.
			motorDc : (int)
				Duty Cycle, portion of on off time per cycle.
			motorFreq : (int)
				Frequncy to pulse off/on to motors.
			irSensor : (irSensor)
				infrared sensor to check for objects being backed into.
			led : (LED_Flasher)
				led flasher, to indicate program is running.
			spk : (toneEmitter)
				The horn!
		"""

		self.rightMotor = rightMotor
		self.leftMotor = leftMotor
		self.motorDc = rightMotor.dc
		self.motorFreq = rightMotor.freq
		self.irSensor = irSensor
		self.led = led
		self.spk = spk
		led.on()

	def drive(self, direction):
		"""
		Drives the motors forwards or backwards based on direction.

		pass forward or backward as direction to drive.

		Attributes:
			direction : (str)
				Can be forward or backward
		"""

		if direction == "forward":
			self.rightMotor.forward()
			self.leftMotor.forward()
		elif direction == "backward":
			self.rightMotor.backward()
			self.leftMotor.backward()

	def turn(self, direction):
		"""
		Drives one side to turn robot right or left. backing up results
		in steering be reversed.

		Attributes:
			direction : (str)
				Can be right or left.
		"""

		if direction == "right":
			self.leftMotor.stop()
		elif direction == "left":
			self.rightMotor.stop()

	def stop(self):
		"""Stops the motors."""

		self.rightMotor.stop()
		self.leftMotor.stop()

	def checkBack(self):
		if self.irSensor.read():
			self.spk.on()
		else:
			self.spk.off()

	def changeSpeed(self, upDown):
		"""
		Changes the speed the motors are driven at in increments of 5

		Attributes:
			upDown : (str)
				Can be either up or down.
			INC : (int)
				Increment to move duty cycle up or down by.

		"""

		INC = 5
		if upDown == "up":
			if self.motorDc == 100:
				print("Already at full speed!")
			else:
				self.motorDc = self.motorDc + INC
				if self.motorDc > 100:
					self.motorDc = 100
					self.rightMotor.changeSpeed(self.motorDc)
					self.leftMotor.changeSpeed(self.motorDc)
					print("Duty Cycle at: ", self.motorDC)
		elif upDown == "down":
			if self.motorDc == 0:
				print("Already at minimum speed!")
			else:
				self.motorDc = self.motorDc - INC
				if self.motorDc < 0:
					self.motorDc = 0
					self.rightMotor.changeSpeed(self.motorDc)
					self.leftMotor.changeSpeed(self.motorDc)
					print("Duty Cycle at: ", self.motorDc)

	def honk(self, doHonk):
		"""Honks the horn!"""
		if doHonk:
			self.spk.on()
		else:
			self.spk.off()

	def light(self, doLed):
		if doLed:
			self.led.on()
		else:
			self.led.off()

###########################################
### This class is for individual motors ###
###########################################
class Motor:
	"""
	Control DC motor using pwm.

	Attributes:
		forward_pin (int): GPIO Pin, when set high motor rotates forwards.
		backward_pin (int): GPIO Pin, when set high motor rotates backwards.
		enable_pin (int): GPIO Pin, pwm sets speed of motor.
		dc (int): Duty Cycle to run pwm at, controls speed of motor. Default 90.
		freq (int): Frequncy to run pwm pulses at. Default to 100 hz.
		motor (pwm): pwm object to control pwm on enable_pin.
	"""

	def __init__(self,
		forward_pin, backward_pin, enable_pin, dc = 90, freq = 4000):
		"""
		The constructor for Motor class.

		Parameters:
			forward_pin (int): GPIO Pin, when set high motor rotates forwards.
			backward_pin (int): GPIO Pin, when set high motor rotates backwards.
			enable_pin (int): GPIO Pin, pwm sets speed of motor.
			dc (int): Duty Cycle to run pwm at, controls speed of motor.
				Default 90.
			freq (int): Frequncy to run pwm pulses at. Default to 100 hz
		"""

		self.forward_pin = forward_pin
		self.backward_pin = backward_pin
		self.enable_pin = enable_pin
		self.pin_list = [forward_pin,
			backward_pin, enable_pin]
		GPIO.setup(self.pin_list, GPIO.OUT)
		self.dc = dc
		self.freq = freq
		self.motor = GPIO.PWM(enable_pin, freq)
		self.motor.start(dc)

	def forward(self):
		""" Drive motor forward."""

		GPIO.output(self.forward_pin, GPIO.HIGH)
		GPIO.output(self.backward_pin, GPIO.LOW)

	def backward(self):
		""" Drive motor backward."""

		GPIO.output(self.forward_pin, GPIO.LOW)
		GPIO.output(self.backward_pin, GPIO.HIGH)

	def stop(self):
		""" Stop motor."""
		GPIO.output(self.forward_pin, GPIO.HIGH)
		GPIO.output(self.backward_pin, GPIO.HIGH)

	def changeSpeed(self, dc):
		"""
		Change duty cycle to modify motor speed.

		Parameters:
			dc (int): Duty cycle to change to.
		"""

		self.motor.ChangeDutyCycle(dc)

#######################
### IR sensor class ###
#######################
class IrSensor:
	def __init__(self, pin):
		self.ir_pin = pin
		GPIO.setup(pin, GPIO.IN)

	def read(self):
		return GPIO.input(self.ir_pin)

###################
### LED Flasher ###
###################
class Led_Flasher:
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(pin, GPIO.OUT)
		self.dc = 15
		self.freq = 1
		self.flash = GPIO.PWM(pin, self.freq)

	def on(self):
		self.flash.start(self.dc)

	def off(self):
		self.flash.stop()

class ToneEmitter:
	def __init__(self, pin, freq):
		self.pin = pin
		self.freq = freq
		GPIO.setup(pin, GPIO.OUT)
		self.dc = 50
		self.emit = GPIO.PWM(pin, freq)

	def on(self):
		self.emit.start(self.dc)

	def off(self):
		self.emit.stop()
