from typing import List, Optional, Tuple
from word2num.languages.en.word_matcher import WordMatcher
from word2num.number_word_parser import BaseNumberWordParser
from word2num.tokenization import SimpleTokenizer
from .vocabulary import DIGITS, UNITS, WHOLE_NUMBERS


class EnglishNumberWordParser(BaseNumberWordParser):
    """Converts English-language text representations of numbers to numerical values."""

    def __init__(self, fuzzy_threshold: int):
        """Initializes the English number word parser."""
        self.matcher = WordMatcher(fuzzy_threshold)

    def parse(self, text: str) -> Optional[float]:
        """
        Parses a number from the given English text representation.

        :param text: A text representation of a number.
        :return: The numerical value of the text representation or None if parsing fails.
        """
        tokenizer = SimpleTokenizer()
        words = tokenizer.tokenize(text)
        is_negative, words = self._check_and_remove_negative(words)

        if self._has_decimal(words):
            result = self._parse_decimal(words)
        else:
            whole_words, fraction_words = self._separate_whole_and_fraction(
                words)
            whole_part = self._process_word_chunk(whole_words)
            fraction_part = self._parse_fraction(fraction_words)
            if None in {whole_part, fraction_part}:
                return None
            result = whole_part + fraction_part

        return -result if is_negative else result

    def _check_and_remove_negative(self, words: List[str]) -> tuple:
        """Checks if the given word list represents a negative number, and remove the negative signifier if it does."""
        is_negative = self.matcher.match_negative_signifier(words[0])
        if is_negative:
            words.pop(0)
        return is_negative, words

    def _has_decimal(self, words: List[str]) -> bool:
        """Checks if the given word list contains a decimal separator."""
        return self._find_decimal_separator(words) is not None

    def _parse_decimal(self, words: List[str]) -> Optional[float]:
        """Parses a decimal number from the given word list."""
        decimal_word = self._find_decimal_separator(words)
        point_index = words.index(decimal_word)
        integer_words = words[:point_index]
        decimal_words = words[point_index + 1:]

        integer_part = self._process_word_chunk(integer_words)
        decimal_part = self._process_word_chunk(decimal_words)

        if integer_part is None or decimal_part is None:
            return None

        decimal_part = decimal_part / (10 ** len(decimal_words))
        return integer_part + decimal_part

    def _parse_digit_sequence(self, words: List[str]) -> Optional[float]:
        """Parses a sequence of digits from the given word list."""
        digit_strings = []

        for word in words:
            match = self.matcher.match_digit(word)
            digit = DIGITS[match]
            digit_strings.append(str(digit))

        return float(''.join(digit for digit in digit_strings))

    def _process_word_chunk(self, words: List[str]) -> Optional[float]:
        """Parses a chunk of words representing a number."""
        if not words:
            return 0

        words = [word for word in words if word != 'and']

        if all(self._is_digit(word) for word in words):
            return self._parse_digit_sequence(words)

        return self._parse_composite_word_sequence(words)

    def _parse_composite_word_sequence(self, words: List[str]) -> Optional[float]:
        """Parses a composite sequence of number words (e.g. "twenty-three million")."""
        sorted_units = sorted(UNITS.items(), key=lambda x: -x[1])
        unit_names = [unit[0] for unit in sorted_units]

        for unit_name in unit_names:
            word_match = self.matcher.match(unit_name, words)
            if word_match:
                # Parse the parts to the left, which multiply the unit value, and the parts to the right, which add to it.
                index = words.index(word_match)
                left_value = self._process_word_chunk(words[:index])
                right_value = self._process_word_chunk(words[index+1:])

                if None in {left_value, right_value}:
                    # Failed to parse one of the sides, so the result can't be determined.
                    return None
                else:
                    return left_value * UNITS[unit_name] + right_value

        # There are no units in the sequence, so we can assume it's a simple sequence of whole numbers.
        return self._parse_whole_number_sequence(words)

    def _parse_whole_number_sequence(self, words: List[str]) -> Optional[float]:
        """Parses a simple sequence of words representing whole numbers, without any units (e.g. "twenty six")."""
        sum = 0
        for word in words:
            match = self.matcher.match_whole_number(word)
            if match:
                sum += WHOLE_NUMBERS[match]
            else:
                return None

        return sum

    def _separate_whole_and_fraction(self, words: List[str]) -> Tuple[List[str], List[str]]:
        """
        Separates a list of words into whole number and fraction parts.

        :param words: A list of words representing a number.
        :return: A tuple containing two lists: words representing the whole number part and words representing the fraction part.
        """
        if self._is_denominator(words[-1]):
            i = len(words) - 1
            separator_index = None
            while i >= 0:
                if self.matcher.match_fraction_separator(words[i]):
                    separator_index = i
                    break
                i -= 1

            if separator_index is not None:
                return words[:separator_index], words[separator_index + 1:]
            else:
                return words[:i + 1], words[i + 1:]
        else:
            return words, []

    def _parse_fraction(self, words: List[str]) -> Optional[float]:
        """Parses a fraction from the given word list."""
        if not words:
            return 0

        for i in range(len(words)):
            if self._is_denominator(words[i]):
                numerator_words = words[:i]
                denominator_word = words[i]
                numerator = self._parse_numerator(
                    numerator_words) if numerator_words else 1
                return numerator / self.matcher.match_denominator(denominator_word)

    def _parse_numerator(self, words: List[str]) -> Optional[float]:
        """Parses a numerator from the given word list."""
        if len(words) == 1 and self.matcher.match_indefinite_article(words[0]):
            return 1
        else:
            return self._process_word_chunk(words)

    def _is_denominator(self, word: str) -> bool:
        """Checks if the given word represents a denominator."""
        return self.matcher.match_denominator(word) is not None

    def _find_decimal_separator(self, words: List[str]) -> Optional[str]:
        """Find the decimal separator in the given word list."""
        for word in words:
            if self.matcher.match_decimal_separator(word):
                return word
        return None

    def _is_digit(self, word: str) -> bool:
        """Check if the given word represents a digit (0-9)."""
        return self.matcher.match_digit(word)
