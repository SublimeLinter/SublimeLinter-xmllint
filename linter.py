from SublimeLinter.lint import Linter, util
from SublimeLinter.lint.linter import VirtualView


class Xmllint(Linter):
    cmd = 'xmllint --noout ${args} -'
    regex = (
        r'^-:(?P<line>\d+):.+?: (?P<message>[^\r\n]+)'
        r'(\r?\n(?P<context>[^\r\n]*)\r?\n(?P<col>[^\^]*)\^)?'
    )
    multiline = True
    error_stream = util.STREAM_STDERR
    defaults = {
        'selector': 'text.xml'
    }

    def split_match(self, match):
        error = super().split_match(match)

        # The caret prefix is a zero-based byte offset, even when empty.
        if match.group('context') is not None:
            error['col'] = len(match.group('col'))

        return error

    def convert_column(self, line, col, m, vv):
        context = m.get('context')
        if context is not None:
            # The printed window is tool-specific; encoding arithmetic is not.
            start = max(vv.select_line(line).find(context), 0)
            return start + VirtualView(context).col_from_utf8(0, col)
        return super().convert_column(line, col, m, vv)
