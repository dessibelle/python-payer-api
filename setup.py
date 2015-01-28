import os
from distutils.core import setup
from setuptools import find_packages


VERSION = __import__("payer_api").VERSION

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

install_requires = [
    'lxml>=3.0',
]

setup(
    name="python-payer-api",
    description="Python package for interacting with the Payer payments API (http://www.payer.se).",
    version=VERSION,
    author="Simon Fransson",
    author_email="simon@dessibelle.se",
    url="https://github.com/dessibelle/python-payer-api",
    download_url="https://github.com/dessibelle/python-payer-api/archive/%s.tar.gz" % VERSION,
    packages=['payer_api'],
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
    license="MIT",
)
