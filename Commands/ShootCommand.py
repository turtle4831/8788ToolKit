import commands2

import Subsystems.Shooter
import Subsystems.Arm


class ReadyShooter(commands2.Command):
   def __init__(self, shooter:Subsystems.Shooter.Shooter):
      self.shooter = shooter
      super().__init__()

   def initialize(self):
      self.shooter.setVelocities(2000)


   def execute(self):
      pass

class PassiveReadyShooter(commands2.Command):
   def __init__(self, shooter:Subsystems.Shooter.Shooter):
      self.shooter = shooter
      super().__init__()

   def initialize(self):
      self.shooter.setVelocities(1000)


   def execute(self):
      pass