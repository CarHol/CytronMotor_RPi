from enum import Enum

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

        # Always start PWM for pin1, as it's needed for speed control
        self.pwm1 = gpio.PWM(pin1, 100)  # 100 Hz frequency
        self.pwm1.start(0)  # Initialize with 0% duty cycle
        gpio.output(pin2, gpio.LOW)

        if mode == Mode.DIR:
            gpio.output(pin2, gpio.LOW)
        elif mode == Mode.PWM:
            gpio.output(pin2, gpio.LOW)
            gpio.output(pin1, gpio.HIGH)


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

        if self.mode == Mode.DIR:
            if speed >= 0:
                self.gpio.output(self.pin2, self.gpio.LOW)
            else:
                self.gpio.output(self.pin2, self.gpio.HIGH)

            # Set the PWM duty cycle
            pwm_duty_cycle = abs(speed) * 100 / 255
            self.pwm1.ChangeDutyCycle(pwm_duty_cycle)

        elif self.mode == Mode.PWM:
            if speed >= 0:
                self.gpio.output(self.pin1, self.gpio.HIGH)
                self.gpio.output(self.pin2, self.gpio.LOW)
            else:
                self.gpio.output(self.pin1, self.gpio.LOW)
                self.gpio.output(self.pin2, self.gpio.HIGH)

            # Set the PWM duty cycle
            pwm_duty_cycle = abs(speed) * 100 / 255
            self.pwm1.ChangeDutyCycle(pwm_duty_cycle)
            self.pwm2.ChangeDutyCycle(pwm_duty_cycle)

    # Assumes a normalized speed value in the range (-1, 1)
    def setSpeedNorm(self, speed):
        if speed < -1:
            speed = -1
        elif speed > 1:
            speed = 1
        
        abs_speed = speed * 255
        self.setSpeed(abs_speed)

    def cleanup(self):
        if self.mode == Mode.PWM:
            self.pwm1.stop()
            self.pwm2.stop()
        self.gpio.cleanup()
