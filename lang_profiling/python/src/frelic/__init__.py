# -*- coding: utf-8 -*-

import subprocess

__git_label__ = ''
try:
    __git_label__ = subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--short',
            'HEAD'
        ])
except subprocess.CalledProcessError:
    __git_label__ = 'RELEASE'

__version__ = '0.0.0-dev'
__release__ = '{}-{}'.format(__version__, __git_label__).strip()
