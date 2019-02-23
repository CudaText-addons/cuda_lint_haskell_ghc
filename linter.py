from cuda_lint import Linter, util
from os.path import basename


class Ghc(Linter):

    syntax = 'Haskell'
    cmd = ('ghc', '-fno-code', '-Wall', '-Wwarn', '-fno-helpful-errors')
    regex = (
        r'^(?P<filename>[^:]+):'
        r'(?P<line>\d+):(?P<col>\d+):'
        r'\s+(?P<error>error:\s+)?(?P<warning>warning:\s+)?'
        r'(?P<message>.+\n\s{2,}.+$)'
    )
    multiline = True

    # No stdin
    tempfile_suffix = 'hs'

    # ghc writes errors to STDERR
    error_stream = util.STREAM_STDERR

    def split_match(self, match):
        """Override to ignore errors reported in imported files."""
        match, line, col, error, warning, message, near = (
            super().split_match(match)
        )

        match_filename = basename(match.groupdict()['filename'])
        #linted_filename = basename(self.filename)

        if not match_filename.startswith('_CudaLint_'):
            return None, None, None, None, None, '', None

        return match, line, col, error, warning, message, near
