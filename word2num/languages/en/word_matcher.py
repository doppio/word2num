import re
from typing import Iterable, Optional
from thefuzz import fuzz
from .vocabulary import DIGITS, UNITS, WHOLE_NUMBERS, IRREGULAR_DENOMINATORS
from .vocabulary import NEGATIVE_SIGNIFIERS, DECIMAL_SEPARATORS, INDEFINITE_ARTICLES, FRACTION_SEPARATORS


class WordMatcher:
    """
    Matches words with different number-related categories based on a fuzzy threshold
    ranging from 0 to 100, where 0 means no match and 100 means an exact match.
    """

    def __init__(self, fuzzy_threshold):
        self.fuzzy_threshold = fuzzy_threshold

    def get_match_score(self, a: str, b: str) -> int:
        """
        Calculates the fuzzy match score between two strings.

        :param a: First string.
        :param b: Second string.
        :return: A fuzzy match score between 0 and 100, where 0 means no match and 100 means an exact match.
        """
        return fuzz.ratio(a, b)

    def find_exact_match(self, word: str, iterable: Iterable[str]) -> Optional[str]:
        """
        Checks if the word is in the iterable.

        :param word: The word to check.
        :param iterable: The iterable to check in.
        :return: The word if it's in the iterable, else None.
        """
        return word if word in iterable else None

    def find_best_fuzzy_match(self, word: str, iterable: Iterable[str]) -> Optional[str]:
        """
        Finds the best fuzzy match for the word in the iterable.

        :param word: The word to match.
        :param iterable: The iterable to match in.
        :return: The best match if there is one above the fuzzy threshold, else None.
        """
        best_ratio = 0
        best_match = None

        for key in iterable:
            ratio = fuzz.ratio(word, key)

            if ratio == 100:
                return word

            if ratio > best_ratio:
                best_ratio = ratio
                best_match = key

        if best_ratio >= self.fuzzy_threshold:
            return best_match
        else:
            return None

    def match(self, word: str, iterable: Iterable[str]) -> Optional[str]:
        """
        Finds a match for the word in the iterable.

        :param word: The word to match.
        :param iterable: The iterable to match in.
        :return: The match if there is one, else None.
        """
        if self.fuzzy_threshold == 100:
            # If we're not using fuzzy matching, it's more performant to directly check for an exact match.
            return self.find_exact_match(word, iterable)
        else:
            return self.find_best_fuzzy_match(word, iterable)

    def match_unit(self, word: str) -> Optional[str]:
        """
        Matches a word with units vocabulary.

        :param word: Word to match.
        :return: Matched unit or None.
        """
        return self.match(word, UNITS)

    def match_digit(self, word: str) -> Optional[str]:
        """
        Matches a word with digits vocabulary.

        :param word: Word to match.
        :return: Matched digit or None.
        """
        return self.match(word, DIGITS)

    def match_whole_number(self, word: str) -> Optional[str]:
        """
        Matches a word with whole numbers vocabulary.

        :param word: Word to match.
        :return: Matched whole number or None.
        """
        return self.match(word, WHOLE_NUMBERS)

    def match_negative_signifier(self, word: str) -> Optional[str]:
        """
        Matches a word with negative signifiers vocabulary.

        :param word: Word to match.
        :return: Matched negative signifier or None.
        """
        return self.match(word, NEGATIVE_SIGNIFIERS)

    def match_decimal_separator(self, word: str) -> Optional[str]:
        """
        Matches a word with decimal separators vocabulary.

        :param word: Word to match.
        :return: Matched decimal separator or None.
        """
        return self.match(word, DECIMAL_SEPARATORS)

    def match_indefinite_article(self, word: str) -> Optional[str]:
        """
        Matches a word with indefinite articles vocabulary.

        :param word: Word to match.
        :return: Matched indefinite article or None.
        """
        return self.match(word, INDEFINITE_ARTICLES)

    def match_fraction_separator(self, word: str) -> Optional[str]:
        """
        Matches a word with fraction separators vocabulary.

        :param word: Word to match.
        :return: Matched fraction separator or None.
        """
        return self.match(word, FRACTION_SEPARATORS)

    def _match_irregular_denominator(self, word: str) -> tuple:
        """
        Attempts to match the word to an irregular denominator.
        If successful, returns the denominator's value and match score.
        Otherwise, returns (None, 0).

        :param word: Word to match.
        :return: Tuple of matched value and score, or (None, 0) if no match.
        """
        singular_word = word.rstrip('s')
        match_score = 0
        irregular_value = None

        match = self.match(singular_word, IRREGULAR_DENOMINATORS)

        if match:
            irregular_value = IRREGULAR_DENOMINATORS[match]
            match_score = self.get_match_score(singular_word, match)

        return irregular_value, match_score

    def _match_regular_denominator(self, word: str) -> tuple:
        """
        Attempts to match the word to a regular denominator.
        If successful, returns the denominator's value and match score.
        Otherwise, returns (None, 0).

        :param word: Word to match.
        :return: Tuple of matched value and score, or (None, 0) if no match.
        """
        match_score = 0
        regular_value = None

        pattern_match = re.match(r'([A-Z]+)ths?', word, flags=re.IGNORECASE)

        if pattern_match:
            base_word = pattern_match.group(1)
            match = self.match(base_word, WHOLE_NUMBERS)
            if match:
                regular_value = WHOLE_NUMBERS[match]
                if match != word:
                    match_score = self.get_match_score(base_word, match)

        return regular_value, match_score

    def match_denominator(self, word: str) -> float:
        """
        Attempts to match the word to a denominator, considering both regular and irregular forms.
        The denominator with the highest match score is returned. If no match is found, returns None.

        :param word: Word to match.
        :return: Matched denominator value or None.
        """
        irregular_value, irregular_score = self._match_irregular_denominator(
            word)
        regular_value, regular_score = self._match_regular_denominator(word)

        if irregular_score and regular_score:
            return irregular_value if irregular_score > regular_score else regular_value
        elif irregular_score:
            return irregular_value
        elif regular_score:
            return regular_value
        else:
            return None
