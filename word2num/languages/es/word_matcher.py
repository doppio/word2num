import re
from word2num.word_matching.word_matcher import WordMatcher
from .vocabulary import SpanishVocabulary


class SpanishWordMatcher(WordMatcher):
    """
    Matches words with different number-related categories based on a fuzzy threshold
    ranging from 0 to 100, where 0 means no match and 100 means an exact match.
    """

    def __init__(self, fuzzy_threshold):
        super().__init__(SpanishVocabulary(), fuzzy_threshold)

    def _regular_denominator_to_whole_number(self, word: str) -> str:
        """
        Converts a regular denominator word to its equivalent whole number form.
        e.g. "doceavo" -> "doce"

        :param word: Regular denominator word to convert.
        :return: Whole number word equivalent of the denominator, if it exists, else None.
        """
        pattern_match = re.match(r'([A-Z]+)avos?', word, flags=re.IGNORECASE)
        if not pattern_match:
            return None

        base_word = pattern_match.group(1)
        return self.match(base_word, self.vocabulary.whole_numbers)

    def _whole_number_to_regular_denominator(self, word: str) -> str:
        """
        Converts a whole number word to its equivalent regular denominator form using the language's rules.
        This method does not handle irregular denominators that violate the language's usual rules.

        :param word: Whole number word to convert.
        :return: Regular denominator form of the word.
        """
        return word + 'avo'

    def _match_irregular_denominator(self, word: str) -> tuple:
        """
        Attempts to match the word to an irregular denominator.
        If successful, returns the denominator's value and match score.
        Otherwise, returns (None, 0).

        :param word: Word to match.
        :return: Tuple of matched value and score, or (None, 0) if no match.
        """
        # Strip any trailing 's' from the word to match both singular and plural forms of the denominator word.
        singular_word = word.rstrip('s')
        return super()._match_irregular_denominator(singular_word)
