# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import click.testing
import pytest

from rotal import cli


VALID_TEST_CASES = {
    'one_value': ('foo\n', 'foo\t1\n'),
    'two_different_values': (
        'foo\nbar\n',
        'foo\t1\nbar\t1\nfoo\t1\n',
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
