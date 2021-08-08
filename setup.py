#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["pandas==1.3.1",
                "spacy==3.1.1",
                "nltk==3.6.2",
                "loguru==0.5.3",
                "python-dotenv==0.19.0",
                "praw==7.4.0"
                ]

test_requirements = [ ]

setup(
    author="Paul Armstrong",
    author_email='paul.armstrong211@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Simple class using spacy and nltk to identitify stocks and sentiment on Reddit forums",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='reddit_stock_sentiment',
    name='reddit_stock_sentiment',
    packages=find_packages(include=['reddit_stock_sentiment', 'reddit_stock_sentiment.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/paul-armstrong-dev/reddit_stock_sentiment',
    version='0.1.3',
    zip_safe=False,
)
