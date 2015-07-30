# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import click.testing
import pytest

from rotal import cli


@pytest.fixture
def runner():
    return click.testing.CliRunner()


class TestMain(object):

    def test_no_arguments(self, runner):
        result = runner.invoke(cli=cli.main)
        assert result.exit_code == 0
        assert not result.exception
