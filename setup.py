#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
import sys
# Fool distutils to accept more than ASCII
reload(sys).setdefaultencoding('utf-8')

setup(
    name='Minimatic',
    version='1.0',
    description='CSS and Javascript Minification/Combination Upgrade to WebHelpers',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Pedro Algarvio',
    author_email='ufs@ufsoft.org',
    maintainer='Linas Juškevičius',
    maintainer_email='linas@idiles.com',
    install_requires=["Pylons", "WebHelpers", "beaker", "cssutils"],
    tests_require=['nose'],
    test_suite='nose.collector',
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'tests.fixtures']),
    include_package_data=True,
)
