from typing import List, Optional
from word2num.languages.es.vocabulary import SpanishVocabulary
from word2num.languages.es.word_matcher import SpanishWordMatcher
from word2num.parsing.standard_parser import StandardParser
from word2num.word_matching.word_matcher import WordMatcher


class SpanishParser(StandardParser):
    """Converts Spanish-language text representations of numbers to numerical values."""

    def __init__(self, fuzzy_threshold: float):
        super().__init__(SpanishWordMatcher(fuzzy_threshold))

    def _parse_whole_number(self, words: List[str]) -> Optional[float]:
        if not words:
            return 0

        # Skip the "and" in numbers like "one hundred and five"
        words = [word for word in words if word != 'and']
        return super()._parse_whole_number(words)
