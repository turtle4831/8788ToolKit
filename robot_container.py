import commands2
import wpilib
from commands2 import button


from Wrappers import TurtleSubsystem

class robot_container:
    def __init__(self):
        self.subsystems = [TurtleSubsystem.TurtleSubsystem()]
        #self.subsystems.append("subsystem name")


        self.driver1 = wpilib.PS5Controller(1)
        self.driver2 = wpilib.PS5Controller(2)

        self.configureBindings()


    def initSubsystems(self):
        for subsystem in self.subsystems:
            subsystem.init()

    def configureBindings(self):
       pass

    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main {Robot} class.

        :returns: the command to run in autonomous
        """
        return commands2.InstantCommand()
