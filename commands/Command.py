from abc import ABC, abstractmethod


class Command(ABC):
    """
    abstract class for all commands.
    Implemented according to Command design pattern.
    """
    @abstractmethod
    def execute(self):
        """
        executes the command
        :return:
        """
        pass

    @abstractmethod
    def undo(self):
        """
        undoes the command
        :return:
        """
        pass
