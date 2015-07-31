# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import signal
import subprocess
import sys
import time

import click.testing
import pytest

from rotal import cli


VALID_TEST_CASES = {
    'no_value': ('', ''),
    'one_value': ('foo\n', '1\tfoo\n'),
    'two_different_values': (
        """\
foo
bar
""",
        """\
1\tfoo
1\tbar
1\tfoo
"""
    ),
}


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.mark.parametrize(
    argnames='input,output',
    argvalues=[
        values
        for test_id, values in sorted(VALID_TEST_CASES.iteritems())
    ],
    ids=sorted(VALID_TEST_CASES),
)
def test_valid_cases(runner, input, output):
    result = runner.invoke(cli=cli.main, input=input)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output == output


class TestSignalHandling(object):
    """Functional tests for signal handling.

    More context: http://stackoverflow.com/a/26159031/1988505
    """

    def test_handle_broken_pipe(self):
        # Given the program is running
        process = subprocess.Popen(
            args=[sys.executable, '-m', 'rotal'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # XXX: Apparently sleeping is required, otherwise we always get None.
        time.sleep(0.1)
        assert process.poll() is None, process.stderr.read()
        # When a broken pipe signal occurs
        process.send_signal(signal.SIGPIPE)
        time.sleep(0.1)
        # Then the program should exit cleanly
        if process.poll() is None:  # pragma: no cover
            # (Test failed. We should probably clean up.)
            process.terminate()
            time.sleep(0.1)
            if process.poll() is None:
                process.kill()
                time.sleep(0.1)
        # (Negative means exited cleanly due to that signal.) (Unix only!)
        assert process.returncode == -signal.SIGPIPE
