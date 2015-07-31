# -*- coding: utf-8 -*-
"""Handles the invocation of the command."""
from __future__ import absolute_import
from __future__ import unicode_literals

import collections

import click


@click.command()
def main():
    """Get a running count of occurrences from a stream.

    Intended to replace `sort | uniq -c` when the input is a stream.
    """
    stdin = click.get_text_stream('stdin')
    counter = collections.Counter()
    for line in stdin:
        click.clear()
        line = line.rstrip('\n')
        counter[line] += 1
        click.echo(format_output(counter=counter))


def format_output(counter):
    return '\n'.join(get_output_lines(counter=counter))


def get_output_lines(counter):
    return [
        '\t'.join(unicode(x) for x in item)
        for item in counter.iteritems()
    ]
