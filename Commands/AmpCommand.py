import commands2
import wpilib

import Commands.TransferPoseCommand
import Subsystems.Arm


class GoToAmpPose(commands2.Command):
   def __int__(self, arm:Subsystems.Arm.Arm):
      self.arm = arm

   def initialize(self):
      self.arm.ChangeArmPose(Subsystems.ArmPose.Amp)
      super().initialize()

   def execute(self):
      if self.arm.armAtPose():
         self.arm.wristGoToPos()
      self.arm.armGoToPos()
      super()

   def isFinished(self) -> bool:
      return self.arm.armAtPose() and self.arm.wristAtPose()


class AmpScore(commands2.Command):
   def __init__(self,arm:Subsystems.Arm.Arm):
      self.timer = wpilib.Timer()
      self.arm = arm
      super().__init__()


   def initialize(self):
      self.timer.reset()
      super().initialize()

   def execute(self):
      self.arm.Transfer()
      pass

   def end(self, interrupted: bool):
      self.arm.TurnOffTransferMotor()
      commands2.CommandScheduler.getInstance().schedule(Commands.TransferPoseCommand.Transfer(self.arm))
      super().end(interrupted)

   def isFinished(self) -> bool:
      return True if self.timer.get() > 0.5 else False


