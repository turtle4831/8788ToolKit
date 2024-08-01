import commands2
from Wrappers import BallistaBotsSubsystem

class robot_container:
    def __init__(self):
        self.subsystems = [BallistaBotsSubsystem.BallistaBotsSubsystem()]
        #self.subsystems.append("subsystem name")
        pass


    def initSubsystems(self):
        for subsystem in self.subsystems:
            subsystem.init()

