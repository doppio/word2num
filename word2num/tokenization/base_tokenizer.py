from abc import ABC, abstractmethod


class BaseTokenizer(ABC):
    """
    Abstract base class for tokenizers.

    Subclasses of Tokenizer must implement the tokenize() method, which takes
    a string as input and returns a list of strings representing the tokens.
    """

    @abstractmethod
    def tokenize(self, text):
        """
        Split the given text into a list of words that can matched to a known vocabulary.

        :param text: The text to tokenize.
        :return: A list of words.
        """
        pass
