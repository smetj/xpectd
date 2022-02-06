#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_style.py
#

import pycodestyle
from pyflakes import api
from pyflakes import reporter
import black
from pathlib import Path


def test_pep8_conformance():
    """
    Test that we conform to PEP-8
    """

    style = pycodestyle.StyleGuide(ignore=["E501", "W503"], quiet=False)
    result = style.check_files(["xpectd"])
    assert result.total_errors == 0


def test_pyflakes():
    """
    Test code with pyflakes
    """

    assert api.checkRecursive(["xpectd"], reporter._makeDefaultReporter()) == 0


def test_black():
    """
    Test whether code is formatted with black
    """

    for path in Path("xpectd").rglob("*.py"):
        assert not black.format_file_in_place(
            Path(path),
            fast=False,
            mode=black.FileMode(),
        )
