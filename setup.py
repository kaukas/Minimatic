#!/usr/bin/env python
from setuptools import setup, find_packages
import re

setup(
    name='Minimatic',
    version='1.0',
    description='CSS and Javascript Minification/Combination Upgrade to WebHelpers',
    long_description=open('README.txt').read(),
    author='Pedro Algarvio',
    author_email='ufs@ufsoft.org',
    maintainer='Linas Juskevicius',
    maintainer_email='linas@idiles.com',
    install_requires=["Pylons", "WebHelpers", "beaker", "cssutils"],
    tests_require=['nose'],
    test_suite='nose.collector',
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'tests.fixtures']),
    include_package_data=True,
)
