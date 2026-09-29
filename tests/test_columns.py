import importlib
import unittest

import sublime


LinterModule = importlib.import_module('SublimeLinter-xmllint.linter')
Linter = LinterModule.Xmllint


def xmllint_output(source_line, caret_bytes, message='Attribute x redefined'):
    # What `xmllint --noout -` prints: the message, the source line, and a caret
    # line whose position is counted in bytes of the UTF-8 source line.
    return '-:1: parser error : {}\n{}\n{}^\n'.format(message, source_line, ' ' * caret_bytes)


class TestColumns(unittest.TestCase):
    def find_error(self, output):
        linter = Linter(sublime.View(0), {})
        errors = list(linter.find_errors(output))
        self.assertEqual(len(errors), 1, errors)
        return errors[0]

    def test_ascii_line_is_unchanged(self):
        error = self.find_error(xmllint_output('<r><a>eeee</a><b x="1" x="2"/></r>', 28))

        self.assertEqual(error['line'], 0)
        self.assertEqual(error['col'], 28)
        self.assertEqual(error['message'], 'Attribute x redefined')

    def test_two_byte_characters_before_the_error(self):
        # four times U+00E9 (2 bytes each): the caret is 4 columns further right
        error = self.find_error(xmllint_output('<r><a>éééé</a><b x="1" x="2"/></r>', 32))

        self.assertEqual(error['col'], 28)

    def test_four_byte_character_before_the_error(self):
        # U+1F600 is 4 bytes but one character: the caret at byte 28 is at
        # character 25 (the `/` of `<b .../>`)
        error = self.find_error(xmllint_output('<r><a>\U0001F600</a><b x="1" x="2"/></r>', 28))

        self.assertEqual(error['col'], 25)

    def test_error_before_the_non_ascii_text_is_unchanged(self):
        error = self.find_error(xmllint_output('<a x="1" x="2">ééé</a>', 14))

        self.assertEqual(error['col'], 14)

    def test_error_without_a_caret_line_still_matches(self):
        linter = Linter(sublime.View(0), {})
        errors = list(linter.find_errors('-:1: parser error : Document is empty\n'))

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['line'], 0)
        self.assertIsNone(errors[0]['col'])
