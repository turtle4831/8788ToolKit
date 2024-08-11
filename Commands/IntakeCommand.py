import commands2

import Commands.TransferPoseCommand
import Subsystems.Arm


class Intake(commands2.Command):
   def end(self, interrupted: bool):
      self.intake.TurnOffTransferMotor()
      commands2.CommandScheduler.getInstance().schedule(Commands.TransferPoseCommand.Transfer(self.intake))
      super().end(interrupted)

   def isFinished(self) -> bool:
      if self.intake.getIntaked():
         return True


   def __init__(self, intake:Subsystems.Arm.Arm):
      self.intake = intake
      super().__init__()
   def execute(self):

      self.intake.armGoToPos()
      if self.intake.armAtPose():
         self.intake.wristGoToPos()
         self.intake.Intake()
      super().execute()

   def initialize(self):
      self.intake.ChangeArmPose(Subsystems.Arm.ArmPose.Intake)
