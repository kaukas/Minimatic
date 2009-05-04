#!/usr/bin/env python
from setuptools import setup, find_packages
import re

setup(
    name='MinificationWebHelpers',
    version='0.3.0',
    description='CSS and Javascript Minification/Combination Upgrade to WebHelpers',
    long_description=open('README.txt').read(),
    author='Pedro Algarvio & Domen Kozar',
    author_email='ufs@ufsoft.org',
    url='http://docs.fubar.si/minwebhelpers/',
    install_requires=["Pylons", "WebHelpers", "beaker", "cssutils"],
    packages=find_packages(),
    include_package_data=True,
)
