import commands2
import ntcore
import wpilib

import Utils.local_logger
import robot_container


class robot(wpilib.TimedRobot):
    def __init__(self):
        self.robotContainer = robot_container.robot_container()
        self.nt = ntcore.NetworkTableInstance.getDefault()
        self.log = Utils.local_logger.LocalLogger("robot")
        self.scheduler = commands2.CommandScheduler.getInstance()
        super().__init__()
    def init_subsystem(self):
        #create all subsystems here obviously
        #susbsytem.init()
        pass
    def robotInit(self):
        self.auto_selection = wpilib.SendableChooser()
        # self.auto_selection.addOption("Test", autonomous.drive_straight)name of the auto then the command


        try:
            self.robotContainer.initSubsystems()
        except Exception as e:
            self.log.error(f"{e}")

    def robotPeriodic(self):
        try:
            commands2.CommandScheduler.getInstance().run()
        except Exception as e:
            self.log.error(f"{e}")


    def teleopInit(self):
        pass
    def teleopPeriodic(self):
        #commands for teleop here
        pass
    def autonomousInit(self):
        self.auto_selection.getSelected().run()
        pass
    def autonomousPeriodic(self):

        pass
if __name__ == "__main__":
    wpilib.run(robot)