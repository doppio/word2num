from word2num.word_matching.vocabulary import Vocabulary

class SpanishVocabulary(Vocabulary):
    """
    Vocabulary class for Spanish language number word parsing.
    """

    @property
    def digits(self):
        return {
            "cero": 0,
            "uno": 1,
            "dos": 2,
            "tres": 3,
            "cuatro": 4,
            "cinco": 5,
            "seis": 6,
            "siete": 7,
            "ocho": 8,
            "nueve": 9,
        }

    @property
    def whole_numbers(self):
        return {
            **self.digits,
            **self.units,
            **self.definite_articles,
            "un": 1,
            "una": 1,
            "diez": 10,
            "once": 11,
            "doce": 12,
            "trece": 13,
            "catorce": 14,
            "quince": 15,
            "dieciséis": 16,
            "diecisiete": 17,
            "dieciocho": 18,
            "diecinueve": 19,
            "veinte": 20,
            "veintiuno": 21,
            "veintidós": 22,
            "veintitrés": 23,
            "veinticuatro": 24,
            "veinticinco": 25,
            "veintiséis": 26,
            "veintisiete": 27,
            "veintiocho": 28,
            "veintinueve": 29,
            "treinta": 30,
            "cuarenta": 40,
            "cincuenta": 50,
            "sesenta": 60,
            "setenta": 70,
            "ochenta": 80,
            "noventa": 90,
            "cien": 100,
            "ciento": 100,
            "doscientos": 200,
            "trescientos": 300,
            "cuatrocientos": 400,
            "quinientos": 500,
            "seiscientos": 600,
            "setecientos": 700,
            "ochocientos": 800,
            "novecientos": 900,
        }

    @property
    def units(self):
        return {
            "mil": 1000,
            "millón": 10 ** 6,
            "millones": 10 ** 6,
            "billón": 10 ** 12,
            "billones": 10 ** 12,
            "cuatrillón": 10 ** 15,
            "cuatrillones": 10 ** 15,
            "quintillón": 10 ** 18,
            "quintillones": 10 ** 18,
        }

    @property
    def irregular_denominators(self):
        return {
            "mitad": 2,
            "media": 2,
            "medio": 2,
            "tercio": 3,
            "cuarto": 4,
            "quinto": 5,
            "sexto": 6,
            "séptimo": 7,
            "octavo": 8,
            "noveno": 9,
            "décimo": 10,
            "centésimo": 100,
            "milésimo": 1000,
            "millonésimo": 10 ** 6,
            "billonésimo": 10 ** 12,
        }

    @property
    def definite_articles(self):
        return {
            "la": 1,
            "el": 1,
        }

    @property
    def fraction_separators(self):
        return ["y"]

    @property
    def decimal_separators(self):
        return ["punto", "coma"]

    @property
    def negative_signifiers(self):
        return ["menos", "negativo", "negativos", "negativa", "negativas"]

    @property
    def indefinite_articles(self):
        return ["un", "una"]
