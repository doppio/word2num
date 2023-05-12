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

        Args:
            text (str): The input text to tokenize.

        Returns:
            list: A list of strings representing the words.
        """
        pass
