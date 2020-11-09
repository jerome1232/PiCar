#!/usr/bin/env python3
import socket
import subprocess
import logging
import sys
from robot import Robot
from serverSock import Server

def main():
   """
   The main PiCar logic

   This is the main logic to run PiCar.

   Attributes:
      _lenable_pin (int): pin that enables/disables power to left motor.
         Used with pwm to control power level.

      _lforward_pin (int): pin that causes the left motor to turn forward.

      _lbackward_pin (int): pin that causes the left motor to turn backward.

      _lmotor_pins (tuple): list of the above pins.

      _renable_pin (int): pin that enables/disables power to the right motor.
         Used with pwm to control power level.

      _rforward_pin (int): pin that causes the right motor to turn forward.

      _lbacward_pin (int): pin that causes the right motor to turn backward.

      _rmotor_pins (tuple): list of the above pins.

      _motor_freq (int): Frequency at which to run pwm to motors.

      _motor_dc (int): duty cycle at which to run pwm to motors.
         This is equivelant to power level, it's the amount of time the pwm
         pulse is "on".

      _ir_pin (int): pin at which we can sense input from ir sensor.

      _pi_car (robot): The pi car we will control.
   """

   logging.basicConfig(level=logging.INFO)

   # Eventually these will be read from a config file. But not yet
   # Left Motor Pins
   _lenable_pin = 16
   _lforward_pin = 20
   _lbackward_pin = 21
   _lmotor_pins = (_lforward_pin,
                   _lbackward_pin,
                   _lenable_pin)
   # Right Motor Pins
   _renable_pin = 13
   _rforward_pin = 19
   _rbackward_pin = 26
   _rmotor_pins = (_rforward_pin,
                   _rbackward_pin,
                   _renable_pin)
   # Pwm info for motors
   _motor_freq = 4000
   _motor_dc = 100
   # IR sensor pin
   _ir_pin = 17

   # Starting mjpeg_streamer
   _p = subprocess.Popen(["test.sh"],
      stdout = subprocess.DEVNULL,
      stderr = subprocess.DEVNULL)
   logging.info("mjpeg_streamer started as pid" + _p.pid)

   # Creating a robot object
   _pi_car = Robot(_lmotor_pins, _rmotor_pins, _motor_dc, _motor_freq, _ir_pin)

   # Creating a socket server
   _sock = Server()

   # entering retrieval loop
   while True:
      data = _sock.get_data()
      logging.info("data recieved:" + data)
      if data == 'quit' : break
      else : _pi_car.process_data(data)

   # kill mjpeg_streamer
   _p.terminate()


   # # Create a listening socket
   # logging.info("Creating listen socket")
   # _s_address = ('0.0.0.0', 5005)
   # _listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # _listen_sock.bind(_s_address)
   # _listen_sock.listen(1)
   # logging.info("Socket created")

   # logging.info("Starting up socket")
   # # Creating a tcp socket to listen for connections
   # while True:
   #    logging.info("Listening on socket for connections")
   #    (clientsocket, address) = _listen_sock.accept()
   #    logging.info("connection from: %s", address)

   #    hear = True
   #    '''Sentinal value to stop socket listen loop.'''
   #    while hear:
   #       data = clientsocket.recv(5)
   #       if data:
   #          info = data.decode('ascii')
   #          logging.info("Recieved %s", info)
   #          if (info == "q"):
   #                hear = False
   #                logging.info("Quiting")
   #          elif (info == "w"):
   #             _pi_car.forward()
   #          elif (info == "s"):
   #             _pi_car.backward()
   #          elif (info == "a"):
   #             _pi_car.left()
   #          elif (info == "d"):
   #             _pi_car.right()
   #          elif (info == "b"):
   #             _pi_car.modSpeed("left", 80)
   #             _pi_car.modSpeed("right", 30)
   #       else:
   #          print('no data from: ', address)
   #          hear = False

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      sys.exit()
