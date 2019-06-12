#!/usr/bin/env python3
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
			self.rightMotor.forward(self.motorDc)
			self.leftMotor.forward(self.motorDc)
		elif direction == "backward":
			self.rightMotor.backward(self.motorDc)
			self.leftMotor.backward(self.motorDc)

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

###########################################
### This class is for individual motors ###
###########################################
class Motor:
	def __init__(self, forward, backward, enable, dc, freq):
		self.forward = forward
		self.backward = backward
		self.enable = enable
		self.pin_list = [forward, backward, enable]
		GPIO.setup(self.pin_list, GPIO.OUT)
		self.dc = dc
		self.freq = freq
		self.motor = GPIO.PWM(enable, freq)
		self.motor.start(dc)

	def forward(self, dc):
		GPIO.output(self.forward, GPIO.HIGH)
		GPIO.output(self.backward, GPIO.LOW)
		self.motor.ChangeDutyCycle(dc)

	def backward(self, dc):
		GPIO.output(self.forward, GPIO.LOW)
		GPIO.output(self.backward, GPIO.HIGH)
		self.motor.ChangeDutyCycle(dc)

	def stop(self):
		GPIO.output(self.forward, GPIO.HIGH)
		GPIO.output(self.backward, GPIO.HIGH)
		self.motor.ChangeDutyCycle(self.dc)

	def changeSpeed(self, dc):
		self.motor.ChangeDutyCycle(dc)

	def getState(self):
		print("enable:   ", GPIO.input(self.enable))
		print("forward:  ", GPIO.input(self.forward))
		print("backward: ", GPIO.input(self.backward))

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
