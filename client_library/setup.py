"""Script for creating an installable python library"""

import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="translate_video",
    packages=find_packages(include=["translate_video"]),
    version="0.1.0",
    description="Python library for submitting video translation jobs and fetching their status",
    author="Aditya N Rao",
    requires=["colorama", "requests"],
    long_description=read("README.md"),
)
