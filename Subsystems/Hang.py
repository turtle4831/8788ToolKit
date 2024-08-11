import phoenix6.hardware
import wpilib

import config
from Wrappers.TurtleSubsystem import TurtleSubsystem

class HangState(enum.Enum):
	UP = 1,
	DOWN = 2,
class Hanger(TurtleSubsystem):
	def __init__(self):
		self.state = HangState.DOWN
		self.compressor = wpilib.Compressor(
			config.AirCan,
			wpilib.PneumaticsModuleType.REVPH
		)

		self.doubleSolenoid = wpilib.DoubleSolenoid(config.AirCan,
													moduleType=wpilib.PneumaticsModuleType.REVPH,
													forwardChannel=config.AirForwardChannel,
													reverseChannel=config.AirBackwardChannel,
													)
		super().__init__()



	def Toggle(self):
		match self.state:
			case HangState.UP:
				self.state = HangState.DOWN

			case HangState.DOWN:
				self.state = HangState.UP

	def init(self):
		super().init()

	def periodic(self) -> None:
		match self.state:
			case HangState.UP:
				self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

			case HangState.DOWN:
				self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

		super().periodic()


