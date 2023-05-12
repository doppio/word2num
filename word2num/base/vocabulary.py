from abc import ABC, abstractmethod
from typing import Dict, List


class Vocabulary(ABC):
    """
    Abstract base class that provides language-specific words used to express numbers.
    """

    @property
    @abstractmethod
    def digits(self) -> Dict[str, int]:
        """Dictionary that maps the basic digit words of a language to their numerical values (0-9)."""
        pass

    @property
    @abstractmethod
    def whole_numbers(self) -> Dict[str, int]:
        """Dictionary that maps whole number words of a language to their numerical values."""
        pass

    @property
    @abstractmethod
    def units(self) -> Dict[str, int]:
        """
        Unit words which can be modified by word chunks composed of smaller numbers.
        e.g. In the English example "five hundred thousand", "five" modifies "hundred" to become 500, which modifies "thousand" to become 500,000.
        So "hundred" and "thousand" are both considered units.
        """
        pass

    @property
    @abstractmethod
    def irregular_denominators(self) -> Dict[str, int]:
        """Irregular denominator words that don't follow the langauge's normal rules for forming denominators."""
        pass

    @property
    @abstractmethod
    def fraction_separators(self) -> List[str]:
        """Words that separate the whole number and fraction parts of a text in phrases expressed as fractions."""
        pass

    @property
    @abstractmethod
    def decimal_separators(self) -> List[str]:
        """Words that represent a decimal point separating the whole number and fractional parts of a number."""
        pass

    @property
    @abstractmethod
    def negative_signifiers(self) -> List[str]:
        """Words that indicate a phrase represents a negative number."""
        pass

    @property
    @abstractmethod
    def indefinite_articles(self) -> List[str]:
        """Non-numerical prefix words that can be interpreted as a value of 1."""
        pass
