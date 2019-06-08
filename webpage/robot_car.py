#!/usr/bin/env python3
import sys
import time
import RPi.GPIO as GPIO
import socket
import os
import signal
import subprocess
GPIO.setmode(GPIO.BCM)

class Robot:
    """
    Create a robotic car with two motors, an ir sensor and a speaker.

    Attributes:
        rightMotor : (motorDriver)
            Motor on right side of the car.
        leftMotor : (motorDriver)
            Motor on the left side of the car.
        motorDc : (int)
            Dutycycle to run motors at.
        motorFreq : (int)
            Number of times per second to pulse signal to motors.
        irSensor : (irSensor)
            Check if an object is behind car.
        led : (LED_Flasher)
            Turns on/off a flashing LED.
        spk : (toneEmitter)
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
            rightMotor : (motorDriver)
                The motor/motors on right side.
            leftMotor : (motorDriver)
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
            self.rightMotor.motorForward(self.motorDc)
            self.leftMotor.motorForward(self.motorDc)
        elif direction == "backward":
            self.rightMotor.motorBackward(self.motorDc)
            self.leftMotor.motorBackward(self.motorDc)

    def turn(self, direction):
        """
        Drives one side to turn robot right or left. backing up results
        in steering be reversed.

        Attributes:
            direction : (str)
                Can be right or left.
        """

        if direction == "right":
            self.leftMotor.motorStop()
        elif direction == "left":
            self.rightMotor.motorStop()

    def stop(self):
        """Stops the motors."""

        self.rightMotor.motorStop()
        self.leftMotor.motorStop()

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
                if self.motorDc > 100: self.motorDc = 100
                self.rightMotor.motorModifySpeed(self.motorDc)
                self.leftMotor.motorModifySpeed(self.motorDc)
                print("Duty Cycle at: ", self.motorDC)
        elif upDown == "down":
            if self.motorDc == 0:
                print("Already at minimum speed!")
            else:
                self.motorDc = self.motorDc - INC
                if self.motorDc < 0: self.motorDc = 0
                self.rightMotor.motorModifySpeed(self.motorDc)
                self.leftMotor.motorModifySpeed(self.motorDc)
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
class MotorDriver:
    def __init__(self, forward, backward, enable, dc, freq):
        self.forward = forward
        self.backward = backward
        self.enable = enable
        self.pin_list = [forward, backward, enable]
        GPIO.setup(pin_list, GPIO.OUT)
        self.dc = dc
        self.freq = freq
        self.motor = GPIO.PWM(enable, freq)
        self.motor.start(dc)

    def motorForward(self, dc):
        GPIO.output(self.forward, GPIO.HIGH)
        GPIO.output(self.backward, GPIO.LOW)
        self.motor.ChangeDutyCycle(dc)

    def motorBackward(self, dc):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.HIGH)
        self.motor.ChangeDutyCycle(dc)

    def motorStop(self):
        GPIO.output(self.forward, GPIO.HIGH)
        GPIO.output(self.backward, GPIO.HIGH)
        self.motor.ChangeDutyCycle(self.dc)

    def motorModifySpeed(self, dc):
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
class LED_Flasher:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.dc = 15
        self.freq = 1
        self.flash = GPIO.PWM(pin, freq)

    def on(self):
        self.flash.start(self.dc)

    def off(self):
        self.flash.stop()

class toneEmitter:
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
    ir_pin= 17  ### PLACEHOLDER VALUE, NOT TRUE PIN
    ## Blue LED
    led_pin = 27 ### PLACE HOLDER VALUE, NOT TRUE PIN
    ## Tone emitter
    spk_pin = 32 ### PLACE HOLDER VALUE, NOT TRUE PIN
    tone = 440 ### Hertz to drive speaker at

    ##################################
    # Creating left and right motors #
    ##################################
    left_motor = MotorDriver(lforward_pin, lbackward_pin, lenable_pin,
            motorDc, motorFreq)
    right_motor = MotorDriver(rforward_pin, rbackward_pin, renable_pin,
            motorDc, motorFreq)
    ##########################################
    ### Creating IR sensor and LED flasher ###
    ##########################################
    irSensor = IrSensor(ir_pin)
    led = LED_Flasher(led_pin)
    ########################
    ### Creating speaker ###
    ########################
    spk = toneEmmitter(spk_pin, tone)
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
