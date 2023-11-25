from typing import List, Optional, Tuple

from word2num.parsing.parser import Parser
from word2num.tokenization import SimpleTokenizer
from word2num.word_matching.word_matcher import WordMatcher


class StandardParser(Parser):
    """
    Converts text representations of numbers to numerical values.
    This a parser that can be used across languages that structure
    number phrases in way that is fundamentally similar to English.
    """

    def __init__(self, word_matcher: WordMatcher):
        """Initializes the standard number word parser."""
        self.matcher = word_matcher

    def parse(self, text: str) -> Optional[float]:
        """
        Parses a number from the given text representation.

        :param text: A text representation of a number.
        :return: The numerical value of the text representation or None if parsing fails.
        """
        tokenizer = SimpleTokenizer()
        words = tokenizer.tokenize(text)
        is_negative, words = self._find_and_remove_negative_signifier(words)

        if self._find_decimal_separator(words):
            result = self._parse_decimal_number(words)
        else:
            result = self._parse_non_decimal_number(words)

        if result is None:
            return None

        return -result if is_negative else result

    def _find_and_remove_negative_signifier(self, words: List[str]) -> tuple:
        """Checks if the given word list represents a negative number, and remove the negative signifier if it does."""
        is_negative = self.matcher.match_negative_signifier(words[0])
        if is_negative:
            words.pop(0)
        return is_negative, words

    def _parse_decimal_number(self, words: List[str]) -> Optional[float]:
        """Parses a list of number words containing a decimal separator (e.g. "one point two")."""
        decimal_word = self._find_decimal_separator(words)
        separator_index = words.index(decimal_word)
        integer_words = words[:separator_index]
        decimal_words = words[separator_index + 1 :]

        integer_part = self._parse_whole_number(integer_words)
        decimal_part = self._parse_whole_number(decimal_words)

        if None in {integer_part, decimal_part}:
            return None

        return integer_part + decimal_part / (10 ** len(decimal_words))

    def _parse_whole_number(self, words: List[str]) -> Optional[float]:
        """Parses a number that does not have a separate fractional component."""
        if not words:
            return 0

        if all(self.matcher.match_digit(word) for word in words):
            # The words are a series of digits (e.g. "one two three").
            return self._parse_digit_sequence(words)

        return self._parse_whole_number_sequence(words)

    def _parse_digit_sequence(self, words: List[str]) -> Optional[float]:
        """Parses a sequence of digits from the given word list."""
        digit_strings = []

        for word in words:
            digit = self.matcher.match_digit(word)
            digit_string = str(self.matcher.vocabulary.digits[digit])
            digit_strings.append(digit_string)

        digit_sequence = float("".join(digit_strings))
        return digit_sequence

    def _parse_whole_number_sequence(self, words: List[str]) -> Optional[float]:
        """Parses a sequence of whole number words potentially including units (e.g. "twenty-three million")."""
        # Sort units in decreasing order of their numerical value
        sorted_units = sorted(
            self.matcher.vocabulary.units.items(), key=lambda x: -x[1]
        )
        unit_names = [unit[0] for unit in sorted_units]

        for unit_name in unit_names:
            word_match = self.matcher.match(unit_name, words)
            if word_match:
                index = words.index(word_match)
                left_value = self._parse_whole_number(words[:index])
                right_value = self._parse_whole_number(words[index + 1 :])

                if None in {left_value, right_value}:
                    return None
                else:
                    return (
                        left_value * self.matcher.vocabulary.units[unit_name]
                        + right_value
                    )

        # No units in the sequence, so it's a simple sequence of whole numbers.
        return self._parse_simple_whole_number_sequence(words)

    def _parse_simple_whole_number_sequence(
        self, words: List[str]
    ) -> Optional[float]:
        """Parses a simple sequence of whole words representing whole numbers, without any units (e.g. "twenty six")."""
        sum = 0
        for word in words:
            match = self.matcher.match_whole_number(word)
            if match:
                sum += self.matcher.vocabulary.whole_numbers[match]
            else:
                return None

        return sum

    def _parse_non_decimal_number(self, words: List[str]) -> Optional[float]:
        """Parses a non-decimal number from the given word list."""
        whole_words, fraction_words = self._split_whole_and_fraction(words)
        whole_part = self._parse_whole_number(whole_words)
        fraction_part = self._parse_fraction(fraction_words)

        if None in {whole_part, fraction_part}:
            return None
        return whole_part + fraction_part

    def _split_whole_and_fraction(
        self, words: List[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Separates a list of words into whole number and fraction parts.

        :param words: A list of words representing a number.
        :return: A tuple containing two lists: words representing the whole number part and words representing the fraction part.
        """
        if self._is_denominator(words[-1]):
            return self._split_at_fraction_separator(words)
        else:
            return words, []

    def _split_at_fraction_separator(
        self, words: List[str]
    ) -> Tuple[List[str], List[str]]:
        """Splits a list of words at the fraction separator."""
        i = len(words) - 1
        separator_index = None
        while i >= 0:
            if self.matcher.match_fraction_separator(words[i]):
                separator_index = i
                break
            i -= 1

        if separator_index is not None:
            return words[:separator_index], words[separator_index + 1 :]
        else:
            return words[: i + 1], words[i + 1 :]

    def _parse_fraction(self, words: List[str]) -> Optional[float]:
        """Parses a fraction from the given word list."""
        if not words:
            return 0

        for i in range(len(words)):
            if self._is_denominator(words[i]):
                numerator_words = words[:i]
                denominator_word = words[i]
                numerator = self._parse_numerator(numerator_words)
                return numerator / self.matcher.match_denominator(
                    denominator_word
                )

    def _parse_numerator(self, words: List[str]) -> Optional[float]:
        """Parses a numerator from the given word list."""
        if not words:
            # If there are no words, the numerator is 1, such as in the string "half"
            return 1
        elif len(words) == 1 and self.matcher.match_indefinite_article(
            words[0]
        ):
            # There is only one word, and it's an indefinite article, which implies 1 ("a third").
            return 1
        else:
            return self._parse_whole_number(words)

    def _is_denominator(self, word: str) -> bool:
        """Checks if the given word represents a denominator."""
        return self.matcher.match_denominator(word) is not None

    def _find_decimal_separator(self, words: List[str]) -> Optional[str]:
        """Find the decimal separator in the given word list."""
        for word in words:
            if self.matcher.match_decimal_separator(word):
                return word
        return None
