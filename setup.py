from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="word2num",
    version="0.1.2",
    author="Bryson Thill",
    author_email="bryson@streamliners.dev",
    description="Converts numbers expressed in words to numerical values.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doppio/word2num",
    license="MIT",
    packages=find_packages(),
    install_requires=["thefuzz>=0.19.0", "python-Levenshtein>=0.20.4"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Linguistic",
    ],
)
