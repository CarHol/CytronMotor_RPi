# A Motor Driver library for Raspberry Pi
This is a small library for controlling Cytron motor drivers using the GPIO on a Raspberry Pi. It is currently Python only, with the goal of adding ports to other languages in the near future.

## Cytron motor driver Python library
The Python library is a minimal port of the Cytron motor driver Arduino library. Its main addition is dependency injection for GPIO - it does not depend directly on RPi.GPIO, opting instead for injecting a GPIO object in the constructor. This is to enable supplying GPIO simulators instead of actual GPIO when developing on other platforms.