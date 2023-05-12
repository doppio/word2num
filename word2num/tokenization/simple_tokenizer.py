import re
from abc import ABC, abstractmethod
from .base_tokenizer import BaseTokenizer


class SimpleTokenizer(BaseTokenizer):
    """
    SimpleTokenizer splits the input text into individual words.

    It converts the text to lowercase and uses regular expressions
    to extract alphabetic words including accented characters.
    """

    def tokenize(self, text):
        text = text.lower()

        # See https://stackoverflow.com/questions/20690499 for details on the regex
        return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", text)
