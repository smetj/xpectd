#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#
#  Copyright 2021 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

PROJECT = "xpectd"
VERSION = "0.2.0"

install_requires = [
    "falcon==3.0.1",
    "gunicorn==20.1.0",
    "croniter==1.2.0",
    "pyyaml==6.0",
    "jsonschema==4.4.0",
    "gevent==21.12.0",
]

dependency_links = []

try:
    with open("README.md", "rt") as f:
        long_description = f.read()
except IOError:
    long_description = ""


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["-v", "tests/"]
        self.test_suite = True

    def run_tests(self):
        import pytest

        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name=PROJECT,
    version=VERSION,
    description="A webservice with predictable outage behavior.",
    long_description=long_description,
    author="Jelle Smet",
    author_email="development@smetj.net",
    url="https://github.com/smetj/xpectd",
    download_url="https://github.com/smetj/xpectd/tarball/master",
    dependency_links=dependency_links,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    extras_require={
        "test": ["pytest", "pycodestyle", "pyflakes", "black"],
    },
    platforms=["Linux"],
    test_suite="tests.test_xpectd",
    cmdclass={"test": PyTest},
    scripts=[],
    provides=[],
    install_requires=install_requires,
    namespace_packages=[],
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "console_scripts": ["xpectd = xpectd:main"],
    },
)
