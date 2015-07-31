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
    'one_value': ('foo\n', '   1 foo\n'),
    'two_different_values': (
        """\
foo
bar
""",
        """\
   1 foo
   1 bar
   1 foo
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


class TestFormatOutputUniqc(object):

    @pytest.mark.parametrize(
        argnames='ordered_counts,expected',
        argvalues=[
            [[('foo', 1)], '   1 foo'],
            [[('foo', 40)], '  40 foo'],
            [[('foo', 117)], ' 117 foo'],
            [[('foo', 1211)], '1211 foo'],
            [[('bar', 1), ('foo', 2)], '   1 bar\n   2 foo'],
            [
                [('a', 35), ('b', 101), ('c', 13720)],
                """\
  35 a
 101 b
13720 c\
"""],
        ],
        ids=[
            'one_item_one_digit',
            'one_item_two_digits',
            'one_item_three_digits',
            'one_item_four_digits',
            'newline_separates_multiple_items',
            # `uniq -c` uses at most three spaces, and doesn't add more
            #   in order to align other rows that might have less in
            #   the event that a count is greater than four digits.
            'pad_each_line_independently',
        ],
    )
    def test_output(self, ordered_counts, expected):
        # When we format the output for the "<ordered_counts>"
        result = cli.format_output_uniqc(ordered_counts=ordered_counts)
        # Then the output should match "<expected>"
        assert result == expected
