#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

test_deps = [
    'nose',
    'pyinotify',
    'sniffer',
]

setup(
    name = 'remotebot',
    version = '1.0',
    packages = find_packages(),

    install_requires = [
        'tornado',
        'sqlalchemy',
    ],

    extras_require = {
        'testing': test_deps,   # for requirements-dev.txt
    },

    tests_require = test_deps,

    test_suite = 'sniffer.main',


    author = 'Fernando López',
    author_email = 'fernando.e.lopez@gmail.com',
    description = 'Servidor para controlar robots educativos de forma remota',
    license = 'GPLv2',
    keywords = 'robots websockets education programming',
    url = 'http://github.com/fernandolopez/remotebot'
)
