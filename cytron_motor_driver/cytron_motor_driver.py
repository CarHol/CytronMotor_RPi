from enum import Enum
import sys

def eprint(*args, **kwargs):
    """
    Print to standard error stream.
    
    Args:
        *args: Variable-length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    print(*args, file=sys.stderr, **kwargs)

class Mode(Enum):
    PWM = 1
    DIR = 2

class CytronMD():
    def __init__(self, gpio, pin1, pin2, mode):
        """
        Initialize a CytronMD instance.

        Args:
            gpio: GPIO library object.
            pin1: The first control pin.
            pin2: The second control pin.
            mode: The mode of operation (Mode.PWM or Mode.DIR).

        Initializes GPIO pins and sets up the motor driver.
        """
        self.gpio = gpio
        self.pin1 = pin1
        self.pin2 = pin2
        self.mode = mode

        gpio.setup(pin1, gpio.OUT)
        gpio.setup(pin2, gpio.OUT)

    def setSpeed(self, speed):
        """
        Set the motor speed.

        Args:
            speed: Speed value between -255 and 255.

        Sets the motor speed based on the selected mode.
        """
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255

        if self.mode == Mode.PWM_DIR:
            if speed >= 0:
                self.gpio.output(self.pin2, self.gpio.LOW)
            else:
                self.gpio.output(self.pin2, self.gpio.HIGH)

            if speed >= 0:
                self.gpio.output(self.pin1, self.gpio.HIGH)
            else:
                self.gpio.output(self.pin1, self.gpio.LOW)

            # Set the PWM duty cycle
            pwm_duty_cycle = abs(speed) * 100 / 255
            pwm = self.gpio.PWM(self._pin1, 100)  # 100 Hz frequency
            pwm.start(pwm_duty_cycle)

        elif self.mode == Mode.PWM_PWM:
            if speed >= 0:
                self.gpio.output(self.pin1, self.gpio.HIGH)
                self.gpio.output(self.pin2, self.gpio.LOW)
            else:
                self.gpio.output(self._pin1, self.gpio.LOW)
                self.gpio.output(self.pin2, self.gpio.HIGH)

            # Set the PWM duty cycle
            pwm_duty_cycle = abs(speed) * 100 / 255
            pwm1 = self.gpio.PWM(self.pin1, 100)  # 100 Hz frequency
            pwm2 = self.gpio.PWM(self.pin2, 100)  # 100 Hz frequency
            pwm1.start(pwm_duty_cycle)
            pwm2.start(pwm_duty_cycle)

    # Assumes a normalized speed value in the range (-1, 1)
    def setSpeedNorm(self, speed):
        if speed < -1:
            speed = -1
        elif speed > 1:
            speed = 1
        
        abs_speed = speed * 255
        self.setSpeed(abs_speed)

    def cleanup(self):
        self.gpio.cleanup()