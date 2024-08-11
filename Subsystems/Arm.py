import math
from enum import Enum
from Wrappers.TurtleSubsystem import TurtleSubsystem
import rev
import wpilib

import config


class ArmPose(Enum):
   Intake = 1
   Amp = 2
   Transfer = 3
   StartingPose = 4


class Arm(TurtleSubsystem):
   def __init__(self):
      #create motors
      super().__init__()
      self.wrist = rev.CANSparkMax(config.wristCan, rev.CANSparkMax.MotorType.kBrushless)
      self.arm = rev.CANSparkMax(config.armCan, rev.CANSparkMax.MotorType.kBrushless)
      self.intake = rev.CANSparkMax(config.intakeCan, rev.CANSparkMax.MotorType.kBrushless)

      self.wristEncoder = self.wrist.getEncoder()
      self.armEncoder = self.arm.getEncoder()
      self.intakeEncoder = self.intake.getEncoder()

      self.lowerLimit = wpilib.AnalogTrigger(config.lowerLimitSwitchPort)
      self.higherLimit = wpilib.AnalogTrigger(config.higherLimitSwitchPoert)

      self.lowerLimit.setLimitsVoltage(
         config.LimitSwitchLowVoltage,
         config.LimitSwitchHighVoltage
      )
      self.higherLimit.setLimitsVoltage(
         config.LimitSwitchLowVoltage,
         config.LimitSwitchHighVoltage
      )

      self.currentPos = ArmPose.StartingPose

   def ChangeArmPose(self, newPose: ArmPose):
      self.currentPos = newPose

   def armGoToPos(self):
      newState = self.currentPos
      match (newState):
         case ArmPose.Amp:
            self.armEncPos = config.ArmAmpPos
         case ArmPose.Intake:
            self.armEncPos = config.ArmIntakePos
         case ArmPose.Transfer:
            self.armEncPos = config.ArmTransferPos

      if self.checkLimits():
         self.ArmPower = -0.3
      else:
         self.ArmPower = config.armPid.calculate(self.armEncoder.getPosition(), self.armEncPos)

      self.arm.set(self.ArmPower)

   def wristGoToPos(self):
      newState = self.currentPos
      match (newState):
         case ArmPose.Amp:
            self.wristEncPos = config.WristAmpPos
         case ArmPose.Intake:
            self.wristEncPos = config.WristIntakePos
         case ArmPose.Transfer:
            self.wristEncPos = config.WristTransferPos

      self.wristPower = config.wristPid.calculate(self.wristEncoder.getPosition(), self.wristEncPos)

      self.wrist.set(self.wristPower)

   def checkLimits(self) -> bool:
      return True if self.lowerLimit.getTriggerState() or self.higherLimit.getTriggerState() else False

   def armAtPose(self):
      if self.errorTolerance(0.1, self.ArmPower):
         return True

      return False

   def wristAtPose(self):
      if self.errorTolerance(0.1, self.wristPower):
         return True

      return False

   def Intake(self):
      power = config.intakePid.calculate(self.intakeEncoder.getVelocity(), 100) + config.intakeFF.calculate(100,
                                                                                                            math.sqrt(
                                                                                                               100))

      self.intake.set(power)

   def Transfer(self):
      power = config.intakePid.calculate(self.intakeEncoder.getVelocity(), -100) + config.intakeFF.calculate(-100,
                                                                                                            math.sqrt(
                                                                                                               100))

      self.intake.set(power)

   def TurnOffTransferMotor(self):
      self.intake.set(0)
   def alignNote(self):
      """
      aligns note
      :return:
      """
      return None
   def getIntaked(self):
      return self.intake.getOutputCurrent() > config.intakeAmperage

   def errorTolerance(self, tolerance: float, value):
      """

      :param tolerance: negative value
      :param value:
      :return:
      """
      return tolerance <= value <= tolerance.__abs__()
