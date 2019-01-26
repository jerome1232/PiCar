#!/usr/bin/env python3
import sys
import time
import RPi.GPIO as GPIO
import socket
import os
import signal
GPIO.setmode(GPIO.BCM)

#
# robot class, 
# 
# Can drive forward, backward, turn in forwards and backwards ways.
# this simplifies logic later in.
#
class Robot:
    def __init__(self, rightMotor, leftMotor):
        self.rightMotor = rightMotor
        self.leftMotor = leftMotor
        self.motorDc = rightMotor.dc
        self.motorFreq = rightMotor.freq

    def driveForward(self):
        self.rightMotor.motorForward(self.motorDc)
        self.leftMotor.motorForward(self.motorDc)

    def driveBackward(self):
        self.rightMotor.motorBackward(self.motorDc)
        self.leftMotor.motorBackward(self.motorDc)

    def motorRightF(self):
        self.rightMotor.motorForward(self.motorDc)
    
    def motorRightB(self):
        self.rightMotor.motorBackward(self.motorDc)
                
    def motorLeftF(self):
        self.leftMotor.motorForward(self.motorDc)
        
    def motorLeftB(self):
        self.leftMotor.motorBackward(self.motorDc)

    def stop(self):
        self.rightMotor.motorStop()
        self.leftMotor.motorStop()

    def accelerate(self):
        if self.motorDc == 100:
            print("Already at full speed!")
        else:
            self.motorDc = self.motorDc + 10
            if self.motorDc > 100: self.motorDc = 100
            self.rightMotor.motorModifySpeed(self.motorDc)
            self.leftMotor.motorModifySpeed(self.motorDc)
            print("Duty Cycle at: ", self.motorDC)

    def deccelerate(self):
        if self.motorDc == 0:
            print("Already at minimum speed!")
        else:
            self.motorDc = self.motorDc - 10
            if self.motorDc < 0: self.motorDc = 0
            self.rightMotor.motorModifySpeed(self.motorDc)
            self.leftMotor.motorModifySpeed(self.motorDc)
            print("Duty Cycle at: ", self.motorDc)
            
#
# This class is for individual motors
#

class MotorDriver:
    def __init__(self, forward, backward, enable, dc, freq):
        self.forward = forward
        self.backward = backward
        self.enable = enable
        self.pin_list = [forward, backward, enable]
        GPIO.setup(self.pin_list, GPIO.OUT)
        self.dc = dc
        self.freq = freq
        self.motor = GPIO.PWM(enable, self.freq)
        self.motor.start(self.dc)

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
    rforward_pin = 26
    rbackward_pin = 19 
    ## Motor Duty cycle and frequncy
    motorFreq = 60
    motorDc = 100
    ##################################
    # Creating left and right motors #
    ##################################
    left_motor = MotorDriver(lforward_pin, lbackward_pin, lenable_pin,
            motorDc, motorFreq)
    right_motor = MotorDriver(rforward_pin, rbackward_pin, renable_pin,
            motorDc, motorFreq)
    #############################
    ### Creating robot object ###
    #############################
    car = Robot(left_motor, right_motor)

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
    isW = False
    isA = False
    isD = False
    isS = False
    isQ = False
    isR = False
    isF = False
    isSpace = False
    
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
                        isR == True
                elif data == 'fDown':
                        isF == True
                elif data == 'qDown':
                        isQ == True
                elif data == 'wUp':
                        isW = False
                elif data == 'sUp':
                        isS = False
                elif data == 'aUp':
                        isA = False
                elif data == 'dUp':
                        isD = False
        
        if isW:
                if isA:
                        car.motorRightF()
                elif isD:
                        car.motorLeftF()
                else:
                        car.driveForward()
        elif isS:
                if isA:
                        car.motorRightB()
                elif isD:
                        car.motorLeftB()
                else:
                        car.driveBackward()
        else:
                car.stop()
        time.sleep(.01)
    car.stop()
    GPIO.cleanup()
    
# Running main
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
