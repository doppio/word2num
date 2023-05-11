from setuptools import setup, find_packages

setup(
    name="word2num",
    version="0.1.0",
    author="Bryson Thill",
    author_email="bryson@streamliners.dev",
    description="Converts numbers expressed in words to numerical values.",
    url="https://github.com/doppio/word2num",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "thefuzz>=0.19.0",
        "python-Levenshtein>=0.20.4"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Linguistic",
    ],
)
