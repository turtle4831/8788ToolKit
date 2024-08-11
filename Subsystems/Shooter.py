import math

import rev
import wpimath.controller
from wpimath._controls._controls.controller import PIDController

import config
from Wrappers import TurtleMotor
from Wrappers.TurtleMotor import PID_CONTROL_TYPE
from Wrappers.TurtleSubsystem import TurtleSubsystem


class Shooter(TurtleSubsystem):
   def __init__(self):
      #motors
      self.leftMotor = TurtleMotor.TurtleMotor(
         motorRev=rev.CANSparkMax(config.leftShooterCan, rev.CANSparkMax.MotorType.kBrushless),
         motor_type=TurtleMotor.MotorType.NEO
      )
      self.rightMotor = TurtleMotor.TurtleMotor(
         motorRev=rev.CANSparkMax(config.rightShooterCan, rev.CANSparkMax.MotorType.kBrushless),
         motor_type=TurtleMotor.MotorType.NEO,
         reverse=True
      )
      self.wantedVelocity = 0
      self.feedforward = wpimath.controller.SimpleMotorFeedforwardRadians(0,config.shooterKv,0)
      super().__init__()
   def setVelocities(self, newVelocity):
      self.wantedVelocity = newVelocity
      self.leftSpeed = config.shooterPid.calculate(self.leftMotor.getVelocity(), newVelocity)
      self.rightSpeed = config.shooterPid.calculate(self.rightMotor.getVelocity(),newVelocity)

      self.leftMotor.setVoltage(self.leftSpeed + self.feedforward.calculate(newVelocity,math.sqrt(newVelocity)))
      self.rightMotor.setVoltage(self.rightSpeed + self.feedforward.calculate(newVelocity,math.sqrt(newVelocity)))

   def atVelocity(self):
      averageError = (self.leftSpeed + self.rightSpeed) / 2
      return self.errorTolerance(.05, averageError)

   def errorTolerance(self, tolerance: float, value):
      """

      :param tolerance: negative value
      :param value:
      :return:
      """
      return tolerance <= value <= tolerance.__abs__()
   def init(self):
      pass


   def periodic(self) -> None:
      pass