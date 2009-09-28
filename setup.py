#!/usr/bin/env python
from setuptools import setup, find_packages
import re

setup(
    name='MinificationWebHelpers',
    version='0.3.5',
    description='CSS and Javascript Minification/Combination Upgrade to WebHelpers',
    long_description=open('README.txt').read(),
    author='Pedro Algarvio',
    author_email='ufs@ufsoft.org',
    maintainer='Domen Kozar',
    maintainer_email='domen@dev.si',
    url='http://docs.fubar.si/minwebhelpers/',
    install_requires=["Pylons", "WebHelpers", "beaker", "cssutils"],
    tests_require=['nose'],
    test_suite='nose.collector',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
)
