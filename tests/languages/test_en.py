import unittest

from word2num import Word2Num


class TestEnglishParser(unittest.TestCase):
    def test_integers(self):
        parse = Word2Num(language_code="en").parse
        self.assertEqual(parse("one"), 1)
        self.assertEqual(parse("twenty three"), 23)
        self.assertEqual(parse("five hundred"), 500)
        self.assertEqual(parse("seven thousand"), 7000)
        self.assertEqual(parse("one hundred and three"), 103)

    def test_decimals(self):
        parse = Word2Num(language_code="en").parse

        self.assertAlmostEqual(parse("one point five"), 1.5)
        self.assertAlmostEqual(parse("three point one four"), 3.14)
        self.assertAlmostEqual(
            parse("twenty-two point zero zero three six"), 22.0036
        )

    def test_fractions(self):
        parse = Word2Num(language_code="en").parse

        self.assertAlmostEqual(parse("one half"), 0.5)
        self.assertAlmostEqual(parse("one and a quarter"), 1.25)
        self.assertAlmostEqual(parse("one and three tenths"), 1.3)
        self.assertAlmostEqual(parse("a third"), 1 / 3)
        self.assertAlmostEqual(parse("three quarters"), 3 / 4)
        self.assertAlmostEqual(parse("five sixteenths"), 5 / 16)

    def test_negatives(self):
        parse = Word2Num(language_code="en").parse

        self.assertEqual(parse("minus eight"), -8)
        self.assertAlmostEqual(parse("negative three fifths"), -3 / 5)

    def test_complex_numbers(self):
        parse = Word2Num(language_code="en").parse

        self.assertEqual(parse("two thousand nine hundred and fifty six"), 2956)
        self.assertEqual(
            parse("fifty-seven thousand four hundred and twenty-one"), 57421
        )
        self.assertEqual(
            parse(
                "one million four hundred and twenty-six thousand nine hundred and eighty-seven"
            ),
            1426987,
        )
        self.assertEqual(
            parse(
                "nine billion nine hundred ninety nine million nine hundred ninety nine thousand nine hundred ninety nine"
            ),
            9999999999,
        )
        self.assertAlmostEqual(
            parse(
                "eight billion six hundred and ninety-four million three hundred thousand one hundred and seventy-two and three-quarters"
            ),
            8694300172.75,
        )

    def test_large_numbers(self):
        parse = Word2Num(language_code="en").parse

        self.assertEqual(parse("one million"), 1000000)
        self.assertEqual(parse("twenty billion"), 20000000000)
        self.assertEqual(parse("three trillion"), 3000000000000)

    def test_small_numbers(self):
        parse = Word2Num(language_code="en").parse

        self.assertAlmostEqual(parse("one thousandth"), 1 / 1000)
        self.assertAlmostEqual(parse("one millionth"), 1 / 1000000)

    def test_digit_sequences(self):
        parse = Word2Num(language_code="en").parse

        self.assertEqual(parse("five five nine two"), 5592)
        self.assertEqual(parse("zero zero one nine two"), 192)
        self.assertEqual(parse("eight two seven nine zero"), 82790)

    def test_misspelled_words(self):
        parse = Word2Num(language_code="en").parse
        extra_fuzzy_parse = Word2Num(
            language_code="en", fuzzy_threshold=60
        ).parse

        self.assertEqual(parse("fivve"), 5)
        self.assertAlmostEqual(parse("onee point fiv"), 1.5)
        self.assertAlmostEqual(parse("thre and a hlf"), 3.5)
        self.assertAlmostEqual(
            extra_fuzzy_parse("twoo hunrdered and twienty-too"), 222
        )
        self.assertAlmostEqual(extra_fuzzy_parse("soxteeeen"), 16)

    def test_unrecognizable_words(self):
        parse = Word2Num(language_code="en").parse
        self.assertIsNone(parse("giraffe"))
        self.assertIsNone(parse("five walruses"))
        self.assertIsNone(parse("one point six capybaras"))

    def test_misspelled_words_no_fuzzy(self):
        parse = Word2Num(language_code="en", fuzzy_threshold=100).parse
        self.assertIsNone(parse("fivve"))


if __name__ == "__main__":
    unittest.main()
