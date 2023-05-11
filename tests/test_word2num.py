import unittest
from word2num import word2num as w2n

class TestWord2Num(unittest.TestCase):
    def test_integers(self):
        self.assertEqual(w2n("one"), 1)
        self.assertEqual(w2n("twenty three"), 23)
        self.assertEqual(w2n("five hundred"), 500)
        self.assertEqual(w2n("seven thousand"), 7000)
        self.assertEqual(w2n("one hundred and three"), 103)

    def test_decimals(self):
        self.assertAlmostEqual(w2n("one point five"), 1.5)
        self.assertAlmostEqual(w2n("three point one four"), 3.14)
        self.assertAlmostEqual(w2n("twenty-two point zero zero three six"), 22.0036)

    def test_fractions(self):
        self.assertAlmostEqual(w2n("one half"), 0.5)
        self.assertAlmostEqual(w2n("one and a quarter"), 1.25)
        self.assertAlmostEqual(w2n("one and three tenths"), 1.3)
        self.assertAlmostEqual(w2n("a third"), 1 / 3)
        self.assertAlmostEqual(w2n("three quarters"), 3 / 4)
        self.assertAlmostEqual(w2n("five sixteenths"), 5 / 16)

    def test_negatives(self):
        self.assertEqual(w2n("minus eight"), -8)
        self.assertAlmostEqual(w2n("negative three fifths"), -3 / 5)

    def test_complex_numbers(self):
      self.assertEqual(w2n("two thousand nine hundred and fifty six"), 2956)
      self.assertEqual(w2n("fifty-seven thousand four hundred and twenty-one"), 57421)
      self.assertEqual(w2n("one million four hundred and twenty-six thousand nine hundred and eighty-seven"), 1426987)
      self.assertEqual(w2n("nine billion nine hundred ninety nine million nine hundred ninety nine thousand nine hundred ninety nine"), 9999999999)
      self.assertAlmostEqual(w2n("eight billion six hundred and ninety-four million three hundred thousand one hundred and seventy-two and three-quarters"), 8694300172.75)
   
    def test_large_numbers(self):
        self.assertEqual(w2n("one million"), 1000000)
        self.assertEqual(w2n("twenty billion"), 20000000000)
        self.assertEqual(w2n("three trillion"), 3000000000000)

    def test_small_numbers(self):
        self.assertAlmostEqual(w2n("one thousandth"), 1 / 1000)
        self.assertAlmostEqual(w2n("one millionth"), 1 / 1000000)

    def test_digit_sequences(self):
        self.assertEqual(w2n("five five nine two"), 5592)
        self.assertEqual(w2n("zero zero one nine two"), 192)
        self.assertEqual(w2n("eight two seven nine zero"), 82790)

    def test_misspelled_words(self):
        self.assertEqual(w2n("fivve"), 5)
        self.assertAlmostEqual(w2n("onee point fiv"), 1.5)
        self.assertAlmostEqual(w2n("thre and a hlf"), 3.5)
        self.assertAlmostEqual(w2n("twoo hunrdered and twienty-too", fuzzy_threshold=60), 222)
        self.assertAlmostEqual(w2n("soxteeeen", fuzzy_threshold=60), 16)

    def test_unrecognizable_words(self):
        self.assertIsNone(w2n("giraffe"))
        self.assertIsNone(w2n("five walruses"))
        self.assertIsNone(w2n("one point six capybaras"))

    def test_misspelled_words_no_fuzzy(self):
        self.assertIsNone(w2n("fivve", fuzzy_threshold=100))

if __name__ == '__main__':
    unittest.main()
