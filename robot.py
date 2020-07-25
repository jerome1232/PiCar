import motor
import irSensor
import logging

class Robot:
   """
   A robot with 2 motors and an ir sensor

   """

   def __init__(self, lMotorPins, rMotorPins, motorDc, motorFreq, ir_pin):
      """Robot constructor."""
      self.rMotor = motor.Motor(rMotorPins[0],
                                rMotorPins[1],
                                rMotorPins[2],
                                motorDc,
                                motorFreq)
      self.lMotor = motor.Motor(lMotorPins[0],
                                lMotorPins[1],
                                lMotorPins[2],
                                motorDc,
                                motorFreq)
      self.ir = irSensor.IrSensor(ir_pin)
      self._status = {
         "status": "stopped",
         "direction": "none"
      }

   def modSpeed(self, motor, dc):
      '''Modifies dc/speed of single motor'''
      if motor == 'right':
         self.rMotor.speed(dc)
         logging.info(f"Robot: Changed right motor speed to {dc}")
      elif motor == 'left':
         self.lMotor.speed(dc)
         logging.info(f"Robot: Changed left motor speed to {dc}")
      else:
         logging.info(f"Robot: {motor} is not a valid motor. Use left/right")

   def forward(self):
      """Drives robot forward."""
      self.rMotor.forward()
      self.lMotor.forward()
      self._status["status"] = "forward"
      logging.info("Robot: Driving both motors forward")


   def backward(self):
      """Drive robot backward."""
      self.rMotor.backward()
      self.lMotor.backward()
      self._status["status"] = "backward"
      logging.info("Robot: Driving both motors backwards")

   def right(self):
      """Turn robot right."""
      if (self._status["status"] == "forward"):
         self.__forward_right()
         self._status["direction"] = "right"
         logging.info("Robot: Turning right while driving forward")
      elif (self._status["status"] == "backward"):
         self.__backward_right()
         self._status["direction"] = "right"
         logging.info("Robot: Turning right while driving backward")
      else:
         self._status["status"] = "stopped"
         self._status["direction"] = "none"
         logging.info("Robot: Not moving, Not turning")

   def left(self):
      """Turn robot left."""
      if (self._status["status"] == "forward"):
         self.__forward_left()
         self._status["direction"] = "left"
         logging.info("Robot: Turning left while driving forward")
      elif (self._status["status"] == "backward"):
         self.__backward_left()
         self._status["direction"] = "left"
         logging.info("Robot: Turning left while driving backward")
      else:
         self._status["status"] = "stopped"
         self._status["direction"] = "none"
         logging.info("Robot: Not moving, Not turning")

   def stop(self):
      """Stop robot."""
      self.lMotor.stop()
      self._status["status"] = "stopped"

   def __forward_right(self):
      """Drives right motor forward, left motor coasts."""
      self.rMotor.forward()
      self.lMotor.coast()

   def __forward_left(self):
      """Drives left motor forward, right motor coasts."""
      self.rMotor.coast()
      self.lMotor.forward()

   def __backward_right(self):
      """Drive right motor backwards, left motor coasts."""
      self.rMotor.backward()
      self.lMotor.coast()

   def __backward_left(self):
      """Drive left motor backwards, right motor coasts."""
      self.rMotor.coast()
      self.lMotor.backward()
