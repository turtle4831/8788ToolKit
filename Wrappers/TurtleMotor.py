from enum import Enum

import phoenix6.hardware
import rev
import wpimath
from wpimath.controller import PIDController,ArmFeedforward,ElevatorFeedforward,SimpleMotorFeedforwardMeters
from Utils import logger


class MotorType(Enum):
    NEO = 0
    NEO_VORTEX = 1
    FALCON = 2
    KRAKEN = 3
    UNKOWN = 4

class PID_CONTROL_TYPE(Enum):
    VELOCITY_CONTROL = 0
    POSITION_CONTROL = 1
class SubsystemType(Enum):
    ELEV_CONTROL = 0
    ARM_CONTROL = 1
    DRIVE_CONTROL = 2
class TurtleMotor:

    def __init__(self,motorRev: rev.CANSparkMax = None,motorCtre: phoenix6.hardware.TalonFX = None, motor_type:MotorType = MotorType.UNKOWN, reverse:bool = False):
        match motor_type:

            case MotorType.KRAKEN:
                self.motorCtre = motorCtre

            case MotorType.FALCON:
                self.motorCtre= motorCtre

            case MotorType.NEO:
                self.motorRev = motorRev
                self.encoderRev = self.motorRev.getEncoder()

            case MotorType.NEO_VORTEX:
                self.motorRev = motorRev
                self.encoderRev = self.motorRev.getEncoder()

        self.motor_type = motor_type
        self.defualt_pid = PIDController(0.001,0,0)
        self.pid_slot = []
        self.pid_slot.append(self.defualt_pid)
        self.feedforward = None
        self.current_slot = 0

        self.ctreSlot0 = phoenix6.configs.Slot0Configs()
        self.ctreSlot1 = phoenix6.configs.Slot1Configs()
        self.ctreSlot2 = phoenix6.configs.Slot2Configs()

        self.controlVelocity = phoenix6.controls.VelocityVoltage(0,0,feed_forward=0)
        self.controlPosition = phoenix6.controls.PositionVoltage(0,0,feed_forward=0)

    def getPosition(self):
        """

        :return: Returns ticks traveled by the motor
        """
        if self.motor_type == MotorType.KRAKEN or self.motor_type == MotorType.FALCON:
            return self.motorCtre.get_position()

        return self.encoderRev.getPosition()

    def setPosition(self,position):
        """

        :param position: new tick value for the motors built in encoder
        :return: CTRE ticks range from -16384 - 16383.999755859375 and rev returns relative ticks
        """
        if self.motor_type == MotorType.KRAKEN or self.motor_type == MotorType.FALCON:
            self.motorCtre.set_position(position)

        return self.encoderRev.setPosition(position)

    def getVelocity(self):
        """
        returns velocity
        :return: both returns in rotations per second
        """
        if self.motor_type == MotorType.KRAKEN or self.motor_type == MotorType.FALCON:
            return self.motorCtre.get_velocity()

        return self.encoderRev.getVelocity() / 60
    def getSlot(self,slot_number:int):
        match slot_number:

            case 0:
                return self.ctreSlot0
            case 1:
               return self.ctreSlot1
            case 2:
                return self.ctreSlot2
    def setPID(self,pid_controller:wpimath.controller.PIDController,slot_number:int):
        """

        :param pid_controller:
        :param slot_number: you can use 0,1,2 for this param anything above or bellow wont set a value
        :return:
        """
        try:
            if slot_number < 0 or slot_number > 2:
                pass
            self.pid_slot.insert(slot_number, pid_controller)
            match slot_number:

                case 0:
                    self.ctreSlot0.with_k_p(pid_controller.getP())
                    self.ctreSlot0.with_k_i(pid_controller.getI())
                    self.ctreSlot0.with_k_d(pid_controller.getD())
                case 1:
                    self.ctreSlot1.with_k_p(pid_controller.getP())
                    self.ctreSlot1.with_k_i(pid_controller.getI())
                    self.ctreSlot1.with_k_d(pid_controller.getD())
                case 2:
                    self.ctreSlot2.with_k_p(pid_controller.getP())
                    self.ctreSlot2.with_k_i(pid_controller.getI())
                    self.ctreSlot2.with_k_d(pid_controller.getD())


        except Exception as e:
            logger.error(f"{e}")


    def controlWithPid(self,measurement:float, setpoint:float = 0, slot:int = 0,control_type:PID_CONTROL_TYPE = None):
        self.power = self.pid_slot[slot].calculate(measurement,setpoint)

        if self.motor_type == MotorType.KRAKEN or self.motor_type == MotorType.FALCON:
            match control_type:
                case PID_CONTROL_TYPE.POSITION_CONTROL:
                    self.motorCtre.set_control(self.controlPosition.with_slot(slot))
                case PID_CONTROL_TYPE.VELOCITY_CONTROL:
                    self.motorCtre.set_control(self.controlVelocity.with_slot(slot))
                case None:
                    pass
        else:
            self.motorRev.set(self.power)


    def setVoltage(self, voltage):
        self.motorRev.set(voltage)





