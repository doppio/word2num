from typing import List, Optional

from word2num.languages.en.word_matcher import EnglishWordMatcher
from word2num.parsing.standard_parser import StandardParser


class EnglishParser(StandardParser):
    """Converts English-language text representations of numbers to numerical values."""

    def __init__(self, fuzzy_threshold: float):
        super().__init__(EnglishWordMatcher(fuzzy_threshold))

    def _parse_whole_number(self, words: List[str]) -> Optional[float]:
        if not words:
            return 0

        # Skip the "and" in numbers like "one hundred and five"
        words = [word for word in words if word != "and"]
        return super()._parse_whole_number(words)
