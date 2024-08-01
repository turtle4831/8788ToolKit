from typing import Generic, TypeVar
import commands2

from Wrappers.BallistaBotsSubsystem import BallistaBotsSubsystem as Subsystem

T = TypeVar("T", bound=Subsystem)


class BasicCommand(commands2.Command):
    """
    Extendable basic command
    """
    ...


class SubsystemCommand(BasicCommand, Generic[T]):
    """
    Extendable subsystem command
    """

    def __init__(self, subsystem: T):
        super().__init__()
        self.subsystem = subsystem
        self.addRequirements(subsystem)