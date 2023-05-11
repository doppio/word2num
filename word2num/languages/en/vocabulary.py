# Vocabulary for English number word parsing

# Basic digits
DIGITS = {
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

# Units representing powers of ten
UNITS = {
    "hundred": 100,
    "thousand": 1000,
    "million": 10 ** 6,
    "billion": 10 ** 9,
    "trillion": 10 ** 12,
    "quadrillion": 10 ** 15,
    "quintillion": 10 ** 18,
}

# Whole numbers, including basic digits and powers of ten
WHOLE_NUMBERS = {
    **DIGITS,
    **UNITS,

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

# Irregular denominator words that don't follow the pattern [WHOLE NUMBER] + [th]
IRREGULAR_DENOMINATORS = {
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

# Words that indicate an expression is negative
NEGATIVE_SIGNIFIERS = {
    "negative",
    "minus",
}

# Words that represent a decimal point
DECIMAL_SEPARATORS = {
    "point",
    "dot",
}

# Non-numerical prefix words that can be interpreted as a value of 1
INDEFINITE_ARTICLES = {
    "a",
    "an",
}

# Words that can separate the whole and fraction parts of a number
FRACTION_SEPARATORS = {
    "and",
}