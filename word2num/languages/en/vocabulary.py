from word2num.word_matching.vocabulary import Vocabulary


class EnglishVocabulary(Vocabulary):
    """
    Vocabulary class for English language number word parsing.
    """

    @property
    def digits(self):
        return {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }

    @property
    def whole_numbers(self):
        return {
            **self.digits,
            **self.units,

            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90,
        }

    @property
    def units(self):
        return {
            "hundred": 100,
            "thousand": 1000,
            "million": 10 ** 6,
            "billion": 10 ** 9,
            "trillion": 10 ** 12,
            "quadrillion": 10 ** 15,
            "quintillion": 10 ** 18,
        }

    @property
    def irregular_denominators(self):
        return {
            "half": 2,
            "quarter": 4,
            "third": 3,
            "fifth": 5,
            "eighth": 8,
            "ninth": 9,
            "twelfth": 12,
            "twentieth": 20,
            "thirtieth": 30,
            "fortieth": 40,
            "fiftieth": 50,
            "sixtieth": 60,
            "seventieth": 70,
            "eightieth": 80,
            "ninetieth": 90,
        }

    @property
    def fraction_separators(self):
        return ["and"]

    @property
    def decimal_separators(self):
        return ["point", "dot"]

    @property
    def negative_signifiers(self):
        return ["negative", "minus"]

    @property
    def indefinite_articles(self):
        return ["a", "an"]
