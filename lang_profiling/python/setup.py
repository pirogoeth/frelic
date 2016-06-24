# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import sys
sys.path.insert(0, os.path.abspath('src/'))

import frelic  # noqa

setup(
    name='frelic',
    version=frelic.__version__,
    description='Frelic profiling agent for Python',

    url='https://github.com/pirogoeth/frelic',
    author='Sean Johnson',
    author_email='pirogoeth@maio.me',

    license='GPLv2',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    install_requires=[
    ],
    include_package_data=True,
    exclude_package_data={
    },
    entry_points={
    },
    test_suite='nose.collector',
    tests_require=[
        'coverage',
        'nose',
    ],
    zip_safe=True
)
