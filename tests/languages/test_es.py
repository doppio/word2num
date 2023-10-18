import unittest
from word2num import Word2Num

LANGUAGE_CODE = "es"


class TestSpanishParser(unittest.TestCase):
    def test_integers(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse
        self.assertEqual(parse("uno"), 1)
        self.assertEqual(parse("veintitrés"), 23)
        self.assertEqual(parse("quinientos"), 500)
        self.assertEqual(parse("siete mil"), 7000)
        self.assertEqual(parse("ciento tres"), 103)

    def test_decimals(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertAlmostEqual(parse("uno punto cinco"), 1.5)
        self.assertAlmostEqual(parse("tres coma uno cuatro"), 3.14)
        self.assertAlmostEqual(
            parse("veintidós punto cero cero tres seis"), 22.0036)

    def test_fractions(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertAlmostEqual(parse("la mitad"), 0.5)
        self.assertAlmostEqual(parse("medio"), 0.5)
        self.assertAlmostEqual(parse("uno y cuarto"), 1.25)
        self.assertAlmostEqual(parse("uno y tres décimos"), 1.3)
        self.assertAlmostEqual(parse("un tercio"), 1 / 3)
        self.assertAlmostEqual(parse("tres cuartas"), 3 / 4)
        self.assertAlmostEqual(parse("cinco dieciseisavos"), 5 / 16)
        self.assertAlmostEqual(parse("un catorceavo"), 1 / 14)

    def test_negatives(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertEqual(parse("menos ocho"), -8)
        self.assertEqual(parse("dos negativo"), -2)
        self.assertAlmostEqual(parse("tres quintas negativas"), -3 / 5)

    def test_complex_numbers(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertEqual(parse(
           "dos mil novecientos cincuenta y seis"), 2956)
        self.assertEqual(
            parse("cincuenta y siete mil cuatrocientos veintiuno"), 57421)
        self.assertEqual(parse(
            "un millón cuatrocientos veintiséis mil novecientos ochenta y siete"), 1426987)
        self.assertEqual(parse(
            "nueve mil novecientos noventa y nueve millones novecientos noventa y nueve mil novecientos noventa y nueve"), 9999999999)
        self.assertAlmostEqual(parse(
            "ocho mil seiscientos noventa y cuatro millones trescientos mil ciento setenta y dos y tres cuartos"), 8694300172.75)

    def test_large_numbers(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertEqual(parse("un millón"), 1000000)
        self.assertEqual(parse("dos mil millones"), 2000000000)
        self.assertEqual(parse("tres billones"), 3000000000000)

    def test_small_numbers(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertAlmostEqual(parse("milésima"), 1 / 1000)
        self.assertAlmostEqual(parse("un millonésimo"), 1 / 1000000)

    def test_digit_sequences(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse

        self.assertEqual(parse("cinco cinco nueve dos"), 5592)
        self.assertEqual(parse("cero cero uno nueve dos"), 192)
        self.assertEqual(parse("ocho dos siete nueve cero"), 82790)

    def test_misspelled_words(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse
        extra_fuzzy_parse = Word2Num(
            language_code=LANGUAGE_CODE,
            fuzzy_threshold=60
        ).parse

        self.assertEqual(parse("quatro"), 4)
        self.assertAlmostEqual(parse("unoo punto cincco"), 1.5)
        self.assertAlmostEqual(parse("tre y medip"), 3.5)
        self.assertAlmostEqual(extra_fuzzy_parse("dociento veintidos"), 222)
        self.assertAlmostEqual(extra_fuzzy_parse("diecises"), 16)

    def test_unrecognizable_words(self):
        parse = Word2Num(language_code=LANGUAGE_CODE).parse
        self.assertIsNone(parse("jirafa"))
        self.assertIsNone(parse("cinco morsas"))
        self.assertIsNone(parse("uno punto seis carpinchos"))

    def test_misspelled_words_no_fuzzy(self):
        parse = Word2Num(
            language_code=LANGUAGE_CODE,
            fuzzy_threshold=100
        ).parse

        self.assertIsNone(parse("cuotro"))


if __name__ == '__main__':
    unittest.main()
