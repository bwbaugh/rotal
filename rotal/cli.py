# -*- coding: utf-8 -*-
"""Handles the invocation of the command."""
from __future__ import absolute_import
from __future__ import unicode_literals

import click


@click.command()
def main():
    """Get a running count of occurrences from a stream.

    Intended to replace `sort | uniq -c` when the input is a stream.
    """
    pass
