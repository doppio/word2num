from abc import ABC, abstractclassmethod
from typing import Iterable, Optional

from thefuzz import fuzz

from .vocabulary import Vocabulary


class WordMatcher(ABC):
    """
    Matches words with different number-related definitions based on a fuzzy threshold
    ranging from 0 to 100, where 0 means no match and 100 means an exact match.
    """

    def __init__(self, vocabulary: Vocabulary, fuzzy_threshold: float):
        self.vocabulary = vocabulary
        self.fuzzy_threshold = fuzzy_threshold

    def get_match_score(self, a: str, b: str) -> int:
        """
        Calculates the fuzzy match score between two strings.

        :param a: First string.
        :param b: Second string.
        :return: A fuzzy match score between 0 and 100, where 0 means no match and 100 means an exact match.
        """
        return fuzz.ratio(a, b)

    def _find_exact_match(
        self, word: str, iterable: Iterable[str]
    ) -> Optional[str]:
        """
        Checks if the word is in the iterable.

        :param word: The word to check.
        :param iterable: The iterable to check in.
        :return: The word if it's in the iterable, else None.
        """
        return word if word in iterable else None

    def _find_best_fuzzy_match(
        self, word: str, iterable: Iterable[str]
    ) -> Optional[str]:
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
        # In most cases, the word will be an exact match, so we check for that first since it's faster.
        if self._find_exact_match(word, iterable):
            return word

        if self.fuzzy_threshold < 100:
            return self._find_best_fuzzy_match(word, iterable)
        else:
            return None

    def match_unit(self, word: str) -> Optional[str]:
        """
        Matches a word with a unit word.

        :param word: Word to match.
        :return: Matched unit word or None.
        """
        return self.match(word, self.vocabulary.units)

    def match_digit(self, word: str) -> Optional[str]:
        """
        Matches a word with a digit word.

        :param word: Word to match.
        :return: Matched digit word or None.
        """
        return self.match(word, self.vocabulary.digits)

    def match_whole_number(self, word: str) -> Optional[str]:
        """
        Matches a word with a whole number word.

        :param word: Word to match.
        :return: Matched whole number word or None.
        """
        return self.match(word, self.vocabulary.whole_numbers)

    def match_negative_signifier(self, word: str) -> Optional[str]:
        """
        Matches a word with a negative signifier.

        :param word: Word to match.
        :return: Matched negative signifier or None.
        """
        return self.match(word, self.vocabulary.negative_signifiers)

    def match_decimal_separator(self, word: str) -> Optional[str]:
        """
        Matches a word with a decimal separator word.

        :param word: Word to match.
        :return: Matched decimal separator word or None.
        """
        return self.match(word, self.vocabulary.decimal_separators)

    def match_indefinite_article(self, word: str) -> Optional[str]:
        """
        Matches a word with a indefinite article.

        :param word: Word to match.
        :return: Matched indefinite article or None.
        """
        return self.match(word, self.vocabulary.indefinite_articles)

    def match_fraction_separator(self, word: str) -> Optional[str]:
        """
        Matches a word with a fraction separator.

        :param word: Word to match.
        :return: Matched fraction separator or None.
        """
        return self.match(word, self.vocabulary.fraction_separators)

    def _match_regular_denominator(self, word: str) -> tuple:
        """
        Attempts to match the word to a regular denominator using the language's
        rules for turning whole numbers into denominators.

        :param word: Word to match.
        :return: Tuple of matched value and score, or (None, 0) if no match.
        """
        denominator_value = None
        match_score = 0

        # Find a matching base word and determine that number's correct denominator form to compare it against `word`.
        base_word = self._regular_denominator_to_whole_number(word)
        if base_word:
            denominator_value = self.vocabulary.whole_numbers[base_word]
            correct_form = self._whole_number_to_denominator(base_word)
            match_score = self.get_match_score(word, correct_form)

        if match_score < self.fuzzy_threshold:
            # It's possible that we found a matching base word but the denominator form fails the fuzzy score requirement.
            return None, 0
        else:
            return denominator_value, match_score

    def _match_irregular_denominator(self, word: str) -> tuple:
        """
        Attempts to match the word to an irregular denominator.
        If successful, returns the denominator's value and match score.
        Otherwise, returns (None, 0).

        :param word: Word to match.
        :return: Tuple of matched value and score, or (None, 0) if no match.
        """
        match_score = 0
        irregular_value = None
        irregular_denominators = self.vocabulary.irregular_denominators
        match = self.match(word, irregular_denominators)

        if match:
            irregular_value = irregular_denominators[match]
            match_score = self.get_match_score(word, match)

        return irregular_value, match_score

    @abstractclassmethod
    def _regular_denominator_to_whole_number(self, word: str) -> str:
        """
        Converts a regular denominator word to its equivalent whole number form.
        e.g. "tenth" -> "ten"

        :param word: Regular denominator word to convert.
        :return: Whole number word equivalent of the denominator, if it exists, else None.
        """
        pass

    @abstractclassmethod
    def _whole_number_to_regular_denominator(self, word: str) -> str:
        """
        Converts a whole number word to its equivalent regular denominator form using the language's rules.
        This method does not handle irregular denominators that violate the language's usual rules.

        :param word: Whole number word to convert.
        :return: Regular denominator form of the word.
        """
        pass

    def _whole_number_to_denominator(self, word: str) -> str:
        """
        Converts a whole number word to its equivalent denominator form.
        This method handles both regular and irregular denominators.

        :param word: Whole number word to convert.
        :return: Denominator form of the word.
        """
        # First check if the word has an irregular denominator form.
        irregular_denominator_values_to_words = {
            v: k for k, v in self.vocabulary.irregular_denominators.items()
        }

        # Get the numerical form of the word to check if it has an irregular denominator form.
        whole_number_value = self.vocabulary.whole_numbers[word]
        if whole_number_value in irregular_denominator_values_to_words:
            return irregular_denominator_values_to_words[whole_number_value]

        # A matching irregular denominator wasn't found, so use the language's default rules for forming the denominator word.
        return self._whole_number_to_regular_denominator(word)

    def match_denominator(self, word: str) -> float:
        """
        Attempts to match the word to a denominator, considering both regular and irregular forms.
        The denominator with the highest match score is returned. If no match is found, returns None.

        :param word: Word to match.
        :return: Matched denominator value or None.
        """
        irregular_match = self._match_irregular_denominator(word)
        irregular_value, irregular_score = irregular_match

        regular_match = self._match_regular_denominator(word)
        regular_value, regular_score = regular_match

        if irregular_score and regular_score:
            # We found both a regular and irregular denominator match, so return the one with the higher score.
            return (
                irregular_value
                if irregular_score > regular_score
                else regular_value
            )
        elif irregular_score:
            return irregular_value
        elif regular_score:
            return regular_value
        else:
            return None
