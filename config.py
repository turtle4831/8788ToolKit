
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

RobotWidth = 3
RobotLength = 3
RobotMaxSpeed = 3

frontLeftCan = 1
frontRightCan =2
backLeftCan = 3
backRightCan = 4
pidgeonCan =5
wristCan = 6
armCan = 7
intakeCan = 8

lowerLimitSwitchPort = 1
higherLimitSwitchPoert =2

LimitSwitchHighVoltage = 14 #fix these
LimitSwitchLowVoltage = -14

leftShooterCan = 6
rightShooterCan = 7
camera1PoseRotation = Rotation3d(#roll pitch yaw in degrees
    0,0,0
)
camera1Pose = Transform3d(#x,y,z in meters
    1,1,1,
    camera1PoseRotation

)

shooterPid = wpimath.controller.PIDController(0,0,0)
shooterKv = 0.075

wristPid = wpimath.controller.PIDController(0.001,0,0)
armPid = wpimath.controller.PIDController(0.001,0,0)
intakePid = wpimath.controller.PIDController(0.001,0,0)
intakeFF = wpimath.controller.SimpleMotorFeedforwardRadians(0,3)

intakeAmperage = 15

robotTimer = wpilib.Timer()


#arm positions
ArmIntakePos = 0
ArmTransferPos =0
ArmAmpPos = 0
ArmStartingPos = 0

WristIntakePos = 0
WristTransferPos = 0
WristAmpPos = 0
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
