import re

from .base_tokenizer import BaseTokenizer


class SimpleTokenizer(BaseTokenizer):
    """
    SimpleTokenizer splits the input text into individual words.

    It converts the text to lowercase and uses regular expressions
    to extract alphabetic words including accented characters.
    """

    def tokenize(self, text):
        text = text.lower()

        # Match all alphabetic words including accented characters.
        # See https://stackoverflow.com/questions/20690499 for details on the regex
        return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", text)
