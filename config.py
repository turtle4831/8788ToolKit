
"""
This file holds all constants such as pid values, setpoints, led values, CAN values etc.
"""
import wpilib
import wpimath.controller
from wpimath.geometry import Transform3d, Rotation3d

from Wrappers.TurtleMotor import MotorType

DEBUG_MODE: bool = False
# MAKE SURE TO MAKE THIS FALSE FOR COMPETITION
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
LOGGING: bool = True
LOG_OUT_LEVEL: int = 0
LOG_FILE_LEVEL: int = 1

isAuto = True
autox=0
autoy=0
autoz=0

RobotWidth = 3
RobotLength = 3
RobotMaxSpeed = 3

WristStartingPos = 0

class MotorConfiguration:
    def __init__(self, motor_type:MotorType):
        #TODO add functionality ie motor max speeds tourqe and recommended velocity
        match motor_type:
            case MotorType.KRAKEN:

                pass
            case MotorType.FALCON:

                pass
            case MotorType.NEO:

                pass
            case MotorType.NEO_VORTEX:
                pass
