
"""
This file holds all constants such as pid values, setpoints, led values, CAN values etc.
"""
from Wrappers.BallistaBotsMotor import MotorType

DEBUG_MODE: bool = False
# MAKE SURE TO MAKE THIS FALSE FOR COMPETITION
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
LOGGING: bool = True
LOG_OUT_LEVEL: int = 0
LOG_FILE_LEVEL: int = 1




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
