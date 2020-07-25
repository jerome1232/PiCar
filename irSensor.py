import RPi.GPIO as GPIO

class IrSensor:
   """
   Access an Infrared Sensor

   Attributes:
      ir_pin (int): pin ir sensor data is at
   """

   def __init__(self, pin):
      """Constructs an infrared sensor object."""
      self.ir_pin = pin
      GPIO.setup(pin, GPIO.IN)

   def read(self):
      """Reads from infrared sensor. Returns 1 if an object is detected"""
      return GPIO.input(self.ir_pin)
