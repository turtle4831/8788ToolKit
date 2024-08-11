import commands2
import wpilib
from commands2 import button

import Commands.IntakeCommand
import Commands.TransferPoseCommand
import Commands.ShootCommand
import Commands.AmpCommand
import Subsystems.Arm
import Subsystems.Drivetrain
import Subsystems.Shooter
import Subsystems.Hang

from Wrappers import TurtleSubsystem

class robot_container:
    def __init__(self):
        self.subsystems = [TurtleSubsystem.TurtleSubsystem()]
        self.arm = Subsystems.Arm.Arm()
        self.drivetrain = Subsystems.Drivetrain.Drivetrain()
        self.shooter = Subsystems.Shooter.Shooter()
        self.hanger = Subsystems.Hang.Hanger()
        #self.subsystems.append("subsystem name")

        self.subsystems.append(self.arm)
        self.subsystems.append(self.drivetrain)
        self.subsystems.append(self.shooter)
        self.subsystems.append(self.hanger)

        self.driver1 = wpilib.PS5Controller(1)
        self.driver2 = wpilib.PS5Controller(2)

        self.configureBindings()


    def initSubsystems(self):
        for subsystem in self.subsystems:
            subsystem.init()

    def configureBindings(self):
        button.Trigger(
            self.driver2.getL2Button()
        ).whileTrue(
                Commands.IntakeCommand.Intake(self.arm)
        )

        button.Trigger(#on press
            self.driver2.getTriangleButtonPressed()
        ).onTrue(
            Commands.AmpCommand.GoToAmpPose().andThen(
                commands2.waitcommand.WaitCommand(0.5).andThen(
                    Commands.AmpCommand.AmpScore(self.arm)
                )
            )
        )

        button.Trigger(
            self.driver1.getCrossButtonPressed()
        ).onTrue(
            commands2.InstantCommand(
                self.hanger.Toggle()
            )
        )

        button.Trigger(
            self.driver2.getR2Button()
        ).onTrue(
            commands2.ConditionalCommand(
                commands2.InstantCommand(self.arm.Transfer()),#tells the arm to pass the note to the shooter
                Commands.ShootCommand.ReadyShooter(self.shooter),
                self.shooter.atVelocity()
            )
        ).onFalse(
            Commands.ShootCommand.PassiveReadyShooter(self.shooter)
        )

    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main {Robot} class.

        :returns: the command to run in autonomous
        """
        return commands2.InstantCommand()
