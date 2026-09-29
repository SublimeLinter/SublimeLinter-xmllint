import importlib
import unittest

import sublime
from SublimeLinter.lint.linter import VirtualView


LinterModule = importlib.import_module('SublimeLinter-xmllint.linter')
Linter = LinterModule.Xmllint


# Real output of `xmllint --noout -` (libxml version 21504) for sources with a repeated attribute.
# libxml2 puts the caret in *bytes* of the UTF-8 line, and prints the source line only up to 80 bytes:
# for longer lines it prints the window that ends at the error, so the caret is relative to that
# window. `col` is the character in the real line where the caret points: the `/` of `<b x="1" x="2"/>`
# for short lines, and the closing quote before it for the long ones (the last character of the window).
CASES = {
    'ascii': {
        'source': '<r><a>eeee</a><b x="1" x="2"/></r>\n',
        'output': '-:1: parser error : Attribute x redefined\n<r><a>eeee</a><b x="1" x="2"/></r>\n                            ^\n',
        'col': 28,
    },
    'two_byte': {
        'source': '<r><a>\xe9\xe9\xe9\xe9</a><b x="1" x="2"/></r>\n',
        'output': '-:1: parser error : Attribute x redefined\n<r><a>\xe9\xe9\xe9\xe9</a><b x="1" x="2"/></r>\n                                ^\n',
        'col': 28,
    },
    'emoji': {
        'source': '<r><a>\U0001f600</a><b x="1" x="2"/></r>\n',
        'output': '-:1: parser error : Attribute x redefined\n<r><a>\U0001f600</a><b x="1" x="2"/></r>\n                            ^\n',
        'col': 25,
    },
    'long_ascii': {
        'source': '<r>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<b x="1" x="2"/></r>\n',
        'output': '-:1: parser error : Attribute x redefined\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<b x="1" x="2"\n                                                                               ^\n',
        'col': 136,
    },
    'long_utf': {
        'source': '<r>\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9<b x="1" x="2"/></r>\n',
        'output': '-:1: parser error : Attribute x redefined\n\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9\xe9<b x="1" x="2"\n                                                                               ^\n',
        'col': 76,
    },
}


class TestColumns(unittest.TestCase):
    def resolve(self, name):
        case = CASES[name]
        linter = Linter(sublime.View(0), {})
        errors = list(linter.find_errors(case['output']))
        self.assertEqual(len(errors), 1, errors)
        m = errors[0]
        line, start, end = linter.reposition_match(m['line'], m['col'], m, VirtualView(case['source']))
        return line, start, case['col']

    def test_ascii_line_is_unchanged(self):
        line, start, expected = self.resolve('ascii')
        self.assertEqual((line, start), (0, expected))

    def test_two_byte_characters_before_the_error(self):
        line, start, expected = self.resolve('two_byte')
        self.assertEqual((line, start), (0, expected))

    def test_four_byte_character_before_the_error(self):
        line, start, expected = self.resolve('emoji')
        self.assertEqual((line, start), (0, expected))

    def test_line_longer_than_the_80_byte_window(self):
        line, start, expected = self.resolve('long_ascii')
        self.assertEqual((line, start), (0, expected))

    def test_long_line_of_two_byte_characters(self):
        line, start, expected = self.resolve('long_utf')
        self.assertEqual((line, start), (0, expected))

    def test_error_without_a_caret_line_still_matches(self):
        linter = Linter(sublime.View(0), {})
        errors = list(linter.find_errors('-:1: parser error : Document is empty' + chr(10)))

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['line'], 0)
        self.assertIsNone(errors[0]['col'])
