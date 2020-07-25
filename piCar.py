# from robot import Robot
import socket
from robot import Robot

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

      _lbacward_pin (int): pin that causes th eright motor to turn backward.

      _rmotor_pins (tuple): list of the above pins.

      _motor_freq (int): Frequency at which to run pwm to motors.

      _motor_dc (int): duty cycle at which to run pwm to motors.
         This is equivelant to power level, it's the amount of time the pwm
         pulse is "on".

      _ir_pin (int): pin at which we can sense input from ir sensor.

      _pi_car (robot): The pi car we will control.
   """


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

   # Creating a robot object
   _pi_car = Robot(_lmotor_pins, _rmotor_pins, _motor_dc, _motor_freq, _ir_pin)

   # Create a listening socket
   _s_address = ('0.0.0.0', 5005)
   _listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   _listen_sock.bind(_s_address)
   _listen_sock.listen(1)

   listen = True

   while listen:
      (clientsocket, address) = _listen_sock.accept()
      try:
         print("connection from: ", address)

         while listen:
            data = clientsocket.recv(16)
            print('received {!r}'.format(data))
            if data:
               print("data")
               info = data.decode('ascii')
               if (info == "q"):
                   listen = False
               elif (info == "w"):
                  _pi_car.forward()
               elif (info == "s"):
                  _pi_car.backward()
               elif (info == "a"):
                  _pi_car.left()
               elif (info == "d"):
                  _pi_car.right()
            else:
               print('no data from: ', address)
               break

      finally:
         _listen_sock.close()

main()