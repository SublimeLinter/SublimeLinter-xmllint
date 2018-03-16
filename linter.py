#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2015-2016 The SublimeLinter Community
# Copyright (c) 2014 Aparajita Fishman
#
# License: MIT
#

"""This module exports the Xmllint plugin class."""

from SublimeLinter.lint import Linter, util


class Xmllint(Linter):
    """Provides an interface to xmllint."""

    syntax = 'xml'
    cmd = 'xmllint --noout * -'
    regex = r'^-:(?P<line>\d+):.+?: (?P<message>[^\r\n]+)(\r?\n[^\r\n]*\r?\n(?P<col>[^\^]*)\^)?'
    multiline = True
    error_stream = util.STREAM_STDERR
