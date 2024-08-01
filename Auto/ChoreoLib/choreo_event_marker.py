from enum import Enum
import commands2


# type of command: sequence, parallel, deadline, race, wait and named
class Command:
    def __init__(self,command_type:str, command_data:list, timestamp:float):
        self.command_type = command_type
        self.data = command_data
        self.timestamp = timestamp

    def getData(self):
        return self.data
    def getCommandType(self):
        return self.command_type
    def getTimestamp(self):
        return self.timestamp


