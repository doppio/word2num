import unittest
from word2num.tokenization import SimpleTokenizer


class SimpleTokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = SimpleTokenizer()

    def test_tokenize(self):
        text = "One, two! Three."
        expected_tokens = ['one', 'two', 'three']
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_empty_text(self):
        text = ""
        expected_tokens = []
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_whitespace_only(self):
        text = "   \t\n"
        expected_tokens = []
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
