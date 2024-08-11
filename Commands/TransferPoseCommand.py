import commands2

import Subsystems.Arm


class Transfer(commands2.Command):
   def __init__(self, intake:Subsystems.Arm.Arm):
      self.intake = intake
      super().__init__()
   def execute(self):

      self.intake.armGoToPos()
      if self.intake.armAtPose():
         self.intake.wristGoToPos()
      super().execute()

   def initialize(self):
      self.intake.ChangeArmPose(Subsystems.Arm.ArmPose.Transfer)
      pass

   def isFinished(self) -> bool:
      return self.intake.armAtPose()