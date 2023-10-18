# word2num 💬 → 🔢 <!-- omit in toc -->

![PyPI Version](https://img.shields.io/pypi/v/word2num?logo=pypi&logoColor=white&style=flat-square)

`word2num` is a Python package for converting numbers expressed in natural language to numerical values. It supports:

- Fractions
- Decimals
- Negative values
- Large numbers into the quintillions
- Digit sequences
- Fuzzy string matching

---

## Table of Contents <!-- omit in toc -->
- [🛠️ Installation](#️-installation)
- [💻 Usage](#-usage)
- [🐻 Fuzzy String Matching](#-fuzzy-string-matching)
  - [Default Fuzzy Threshold](#default-fuzzy-threshold)
  - [Custom Fuzzy Threshold](#custom-fuzzy-threshold)
  - [Disable Fuzzy Matching](#disable-fuzzy-matching)
- [🌐 Language Support](#-language-support)
- [🤝 Contributing](#-contributing)
- [📃 License](#-license)

---


## 🛠️ Installation

To use `word2num`, you must first install it. You can do this using pip by running the following command in your terminal:

```
pip install word2num
```

## 💻 Usage

Once installed, you can use `word2num` to convert numbers expressed in natural language to numerical values. To parse a single string, use the `word2num` convenience function:

```python
from word2num import word2num

word2num("fifty-seven thousand four hundred and twenty-one")  # 57421
```

If you need to parse multiple strings, you can create your own instance of `Word2Num` and call its `parse` method:

```python
from word2num import Word2Num

w2n = Word2Num()
w2n.parse("one hundred and one")     # 101
w2n.parse("seventeen billion")       # 17000000000
w2n.parse("negative eight")          # -8
w2n.parse("half")                    # 0.5
w2n.parse("one and three quarters")  # 1.75
w2n.parse("one three three seven")   # 1337
```

Note that these functions will return `None` if a valid numerical value couldn't be interpreted.

## 🐻 Fuzzy String Matching

`word2num` uses fuzzy string matching to help parse misspelled number words.

### Default Fuzzy Threshold

By default, `word2num` uses a fuzzy threshold of 80, which means that it will match a word to a number if the fuzzy score is 80 or higher.

### Custom Fuzzy Threshold

You can change the fuzzy threshold by passing a `fuzzy_threshold` parameter to the `word2num` function or to the `Word2Num` class constructor:

```python
# Using the word2num function
word2num("soxteeeen", fuzzy_threshold=60) # [16]

# Using the Word2Num class
w2n = Word2Num(fuzzy_threshold=60)
w2n.parse("twoo hunrdered and twienty-too")  # [222]
```

### Disable Fuzzy Matching

To disable fuzzy matching (exact matching only), you can set the `fuzzy_threshold` to 100:

```python
w2n = Word2Num(fuzzy_threshold=100)
w2n.parse("two hundered and twinty-two")  # None
```

## 🌐 Language Support

* English
* Spanish

We'd love to add support for other languages. Contributions are more than welcome, so if you're interested in contributing, see the "Contributing" section below!

## 🤝 Contributing

Contributions to `word2num` are more than welcome! If you'd like to contribute, please follow these guidelines:

- Make sure the tests pass by running `pytest` in the root directory of the repository.
- If appropriate, add new tests to cover your changes.
- Follow the existing code style and conventions.
- Create a pull request with your changes.

## 📃 License

`word2num` is released under the MIT License. See `LICENSE.txt` for more information.
