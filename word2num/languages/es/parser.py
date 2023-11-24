from typing import List, Optional

from word2num.languages.es.word_matcher import SpanishWordMatcher
from word2num.parsing.standard_parser import StandardParser


class SpanishParser(StandardParser):
    """Converts Spanish-language text representations of numbers to numerical values."""

    def __init__(self, fuzzy_threshold: float):
        super().__init__(SpanishWordMatcher(fuzzy_threshold))

    def _parse_whole_number(self, words: List[str]) -> Optional[float]:
        if not words:
            return 0

        # Skip the "y" in numbers like "cinquenta y tres"
        words = [word for word in words if word != "y"]
        return super()._parse_whole_number(words)

    def _find_and_remove_negative_signifier(self, words: List[str]) -> tuple:
        """Checks if the given word list represents a negative number, and remove the negative signifier if it does."""
        is_negative = self.matcher.match_negative_signifier(words[-1])
        if is_negative:
            words.pop()
            return is_negative, words

        return super()._find_and_remove_negative_signifier(words)
