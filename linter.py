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

        # Keep what `reposition_match` needs: the source line as printed by
        # xmllint and the caret offset in it (libxml2 counts it in bytes).
        if match.group('context') is not None:
            error['context'] = match.group('context')
            error['caret_bytes'] = len(match.group('col'))

        return error

    def reposition_match(self, line, col, m, vv):
        context = m.get('context')
        if context is not None:
            # xmllint prints the source line only up to 80 bytes, as the window
            # that ends at the error, and puts the caret in bytes. So look for
            # that window in the real line and convert the offset to characters.
            source = vv.select_line(line)
            start = max(source.find(context), 0)
            caret = context.encode('utf-8')[:m['caret_bytes']].decode('utf-8', 'ignore')
            col = start + len(caret)

        return super().reposition_match(line, col, m, vv)
