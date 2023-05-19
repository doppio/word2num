from typing import Optional

from .languages.es.parser import SpanishParser
from .languages.en import EnglishParser

parsers = {
    "en": EnglishParser,
    "es": SpanishParser,
}


class Word2Num:
    def __init__(self, language_code: str = "en", fuzzy_threshold: int = 80):
        self.exact_converter, self.fuzzy_converter = self._initialize_parsers(
            language_code, fuzzy_threshold)

    @staticmethod
    def _initialize_parsers(language_code: str, fuzzy_threshold: int):
        if language_code in parsers.keys():
            parser_class = parsers[language_code]
            exact_parser = parser_class(fuzzy_threshold=100)
            fuzzy_parser = parser_class(
                fuzzy_threshold) if fuzzy_threshold < 100 else None
            return exact_parser, fuzzy_parser
        else:
            raise ValueError(f"Unsupported language: {language_code}")

    def parse(self, text: str) -> Optional[float]:
        """
        Parses a number from the given text representation.

        :param text: A text representation of a number.
        :return: The numerical value of the text representation or None if parsing fails.
        """
        result = self.exact_converter.parse(text)
        if result or not self.fuzzy_converter:
            return result

        return self.fuzzy_converter.parse(text)

    def __str__(self) -> str:
        return str(self.exact_converter)

    def __repr__(self) -> str:
        return repr(self.exact_converter)


def word2num(text: str, language_code: str = "en", fuzzy_threshold: int = 80) -> Optional[float]:
    """
    Converts a text representation of a number to its numerical value.
    This is a convenience method that creates a Word2Num instance and calls its parse method.
    If you are converting many numbers, it is more efficient to create a Word2Num instance and call its parse method directly.

    :param text: A text representation of a number.
    :param language: The language of the text representation (default: "en" for English).
    :param fuzzy_threshold: The minimum score for fuzzy string matching (default: 80).
    :return: The numerical value of the text representation or None if parsing fails.
    """
    w2n = Word2Num(
        language_code=language_code,
        fuzzy_threshold=fuzzy_threshold
    )

    return w2n.parse(text)
