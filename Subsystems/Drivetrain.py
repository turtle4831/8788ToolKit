import commands2
import phoenix6.hardware
import rev
import wpilib
import wpimath

from wpimath.geometry import Translation2d, Rotation2d, Pose2d
from wpimath.kinematics import MecanumDriveKinematics, ChassisSpeeds
from commands2 import Command

import config
from Wrappers import TurtleMotor, TurtleSubsystem, TurtleCommand


class Drivetrain(TurtleSubsystem):

   def __init__(self):
      self.driver = wpilib.PS5Controller(1)
      self.frontLeft = TurtleMotor.TurtleMotor(
         motorRev=rev.CANSparkMax(config.frontLeftCan, rev.CANSparkMax.MotorType.kBrushless),
         motor_type=TurtleMotor.MotorType.NEO
      )
      self.frontRight = TurtleMotor.TurtleMotor(
         motorRev=rev.CANSparkMax(config.frontRightCan, rev.CANSparkMax.MotorType.kBrushless),
         motor_type=TurtleMotor.MotorType.NEO,
         reverse=True
      )
      self.backLeft = TurtleMotor.TurtleMotor(
         motorRev=rev.CANSparkMax(config.backLeftCan, rev.CANSparkMax.MotorType.kBrushless),
         motor_type=TurtleMotor.MotorType.NEO
      )
      self.backRight = TurtleMotor.TurtleMotor(
         motorRev=rev.CANSparkMax(config.backRightCan, rev.CANSparkMax.MotorType.kBrushless),
         motor_type=TurtleMotor.MotorType.NEO,
         reverse=True
      )
      """
      new Translation2d(LENGTH / 2, WIDTH / 2),
               new Translation2d(LENGTH / 2, -WIDTH / 2),
               new Translation2d(-LENGTH / 2, WIDTH / 2),
               new Translation2d(-LENGTH / 2, -WIDTH / 2)
      """
      self.frontLeftLocation = wpimath.geometry.Translation2d(config.RobotLength / 2, config.RobotWidth / 2)
      self.frontRightLocation = wpimath.geometry.Translation2d(config.RobotLength / 2, -config.RobotWidth / 2)
      self.backLeftLocation = wpimath.geometry.Translation2d(-config.RobotLength, config.RobotWidth / 2)
      self.backRightLocation = wpimath.geometry.Translation2d(-config.RobotLength, -config.RobotWidth / 2)

      self.gyro = phoenix6.hardware.Pigeon2(5, "rio")
      self.wheelPose = wpimath.kinematics.MecanumDriveWheelPositions(
         self.frontLeftLocation, self.frontRightLocation, self.backLeftLocation, self.backRightLocation
      )
      self.kinematics = wpimath.kinematics.MecanumDriveKinematics(
         self.frontLeftLocation, self.frontRightLocation, self.backLeftLocation, self.backRightLocation
      )

      self.odometry = wpimath.kinematics.MecanumDriveOdometry(
         self.kinematics, Rotation2d().fromDegrees(self.getGyroHeading()),
         self.getWheelPose(),
         Pose2d(0, 0, Rotation2d().fromDegrees(0))  # starting pose

      )
      self.frontLeftPIDController = wpimath.controller.PIDController(1, 0, 0)
      self.frontRightPIDController = wpimath.controller.PIDController(1, 0, 0)
      self.backLeftPIDController = wpimath.controller.PIDController(1, 0, 0)
      self.backRightPIDController = wpimath.controller.PIDController(1, 0, 0)

      self.feedforward = wpimath.controller.SimpleMotorFeedforwardMeters(1, 3)#tune all these

   def resetOdometry(self, newpose: Pose2d):
      pos = wpimath.kinematics.MecanumDriveWheelPositions()
      pos.frontLeft = 0
      pos.frontRight = 0
      pos.rearLeft = 0
      pos.rearRight = 0
      self.odometry.resetPosition(Rotation2d().fromDegrees(self.getGyroHeading()),
                                  0,
                                  newpose)
   def getWheelPose(self):
      pos = wpimath.kinematics.MecanumDriveWheelPositions()
      pos.frontLeft = self.frontLeft.getPosition()
      pos.frontRight = self.frontRight.getPosition()
      pos.rearLeft = self.frontLeft.getPosition()
      pos.rearRight = self.backRight.getPosition()
      return pos


   def updateOdometry(self):
      self.odometry.update(
         Rotation2d().fromDegrees(self.getGyroHeading()),
         self.getWheelPose()
      )

   def getGyroHeading(self):
      return self.gyro.get_yaw().value_as_double  # might need to fix this idk tho

   def setSpeeds(self, speeds: wpimath.kinematics.MecanumDriveWheelSpeeds):
      """Sets the desired speeds for each wheel."""
      frontLeftFeedforward = self.feedforward.calculate(speeds.frontLeft)
      frontRightFeedforward = self.feedforward.calculate(speeds.frontRight)
      backLeftFeedforward = self.feedforward.calculate(speeds.rearLeft)
      backRightFeedforward = self.feedforward.calculate(speeds.rearRight)

      frontLeftOutput = self.frontLeftPIDController.calculate(
         self.frontLeft.getVelocity(), speeds.frontLeft
      )
      frontRightOutput = self.frontRightPIDController.calculate(
         self.frontRight.getVelocity(), speeds.frontRight
      )
      backLeftOutput = self.frontLeftPIDController.calculate(
         self.backLeft.getVelocity(), speeds.rearLeft
      )
      backRightOutput = self.frontRightPIDController.calculate(
         self.backRight.getVelocity(), speeds.rearRight
      )

      self.frontLeft.setVoltage(frontLeftOutput + frontLeftFeedforward)
      self.frontRight.setVoltage(frontRightOutput + frontRightFeedforward)
      self.backLeft.setVoltage(backLeftOutput + backLeftFeedforward)
      self.backRight.setVoltage(backRightOutput + backRightFeedforward)

   def drive(self,xspeed, yspeed, rot,periodSeconds):
      mecanumDriveWheelSpeeds = self.kinematics.toWheelSpeeds(
         ChassisSpeeds.discretize(
            ChassisSpeeds(xspeed,yspeed,rot),
            periodSeconds
         )
      )
      mecanumDriveWheelSpeeds.desaturate(config.RobotMaxSpeed)
      self.setSpeeds(mecanumDriveWheelSpeeds)

   def DriveCommand(self,autoX=0,autoY=0,autoZ=0):

      return commands2.ConditionalCommand(
         commands2.Command(#if auto
            lambda: self.drive(
               autoX,
               autoY),
               autoZ,
               config.robotTimer.get()
            )
      ,commands2.RunCommand(
            lambda: self.drive(
               self.driver.getLeftX(),
               self.driver.getLeftY(),
               self.driver.getRightX(),
               config.robotTimer.get()
            )
         ),config.isAuto
      )


   def resetTimer(self):
      config.robotTimer.reset()

   def init(self):
      self.resetTimer()
      commands2.CommandScheduler.getInstance().setDefaultCommand(
         self,
         self.DriveCommand()
      )
      super().init()

   def periodic(self):
      super.__init__()

   def setDefaultCommand(self, command: Command) -> None:
      super().setDefaultCommand(command)
