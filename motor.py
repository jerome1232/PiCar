import RPi.GPIO as GPIO

class Motor:
    """
    Contorl DC motor using pwm

    Attributes:
    forward_pin (int): GPIO Pin, when set high motor rotates forwards.
    backward_pin (int): GPIO Pin, when set hihg motor rotates backwards.
    enable_pin (int): GPIO Pin, pwm sets speed of motor.
    dc (int): Duty cycle to run pwm at, the amount of time motor is on per pwm pulse. Default is 90.
    freq (init): Frequency to run pwm puleses at, default is 100hz.
    motor (pwm): pwm object to control pwm on enable_pin
    """

    def __init__(self, forward_pin, backward_pin, enable_pin, dc = 90, freq = 4000):
        """
        The constructor for Motor

        Parameters:
            forward_pin (int): GPIO Pin, when set high motor rotates forwards.
            backward_pin (int): GPIO Pin, when set hihg motor rotates backwards.
            enable_pin (int): GPIO Pin, pwm sets speed of motor.
            dc (int): Duty cycle to run pwm at, the amount of time motor is on per pwm pulse.
            Default is 90.

            freq (init): Frequency to run pwm puleses at, default is 100hz.
        """
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.enable_pin = enable_pin
        self.pin_list = [forward_pin, backward_pin, enable_pin]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_list, GPIO.OUT)
        self.dc = dc
        self.freq = freq
        self.pwm = GPIO.PWM(enable_pin, freq)
        self.pwm.start(dc)

    def __del__(self):
        """The Destructor for Motor."""
        self.pwm.stop()
        GPIO.setup(self.pin_list, GPIO.IN)

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

    def coast(self):
        """ Let motor coast."""
        GPIO.output(self.forward_pin, GPIO.LOW)
        GPIO.output(self.backward_pin, GPIO.LOW)

    def speed(self, dc):
        """ Modify motor speed.

            params:
                dc (int): Short for duty cycle you can think of this
                    as a percentage of time the motor is on.:
        """
        self.pwm.ChangeDutyCycle(dc)
