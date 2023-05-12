import re
from abc import ABC, abstractmethod
from .base_tokenizer import BaseTokenizer


class SimpleTokenizer(BaseTokenizer):
    """
    SimpleTokenizer splits the input text into individual words.

    It converts the text to lowercase, removes commas,
    and uses regular expressions to extract alphanumeric words.
    """

    def tokenize(self, text):
        text = text.lower().replace(',', ' ')
        return re.findall(r"\w+", text)
