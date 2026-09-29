from SublimeLinter.lint import Linter, util


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

        # libxml2 positions the caret in *bytes* of the UTF-8 source line, but
        # we need a column in characters. Convert using the printed line.
        context = match.group('context')
        if error.col and context:
            error['col'] = len(context.encode('utf-8')[:error.col].decode('utf-8', 'ignore'))

        return error
