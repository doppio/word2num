from abc import ABC, abstractmethod
from typing import Optional


class Parser(ABC):
    """Abstract Base Class for a parser that converts textual representations of numbers into numerical values."""

    @abstractmethod
    def parse(self, text: str) -> Optional[float]:
        """
        Parses a number from the given text representation.

        :param text: A text representation of a number.
        :return: The numerical value of the text representation or None if parsing fails.
        """
        pass

    def __str__(self) -> str:
        """Returns a string representation of the class."""
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        """Returns a formal string representation of the class."""
        return self.__str__()
