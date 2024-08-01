import commands2
from commands2 import Command


class BallistaBotsSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()

    def init(self):
        pass

    def periodic(self) -> None:
        super().periodic()

    def setDefaultCommand(self, command: Command) -> None:
        super().setDefaultCommand(command)


