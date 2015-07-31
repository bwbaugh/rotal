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
    counter = collections.Counter()
    for line in click.get_text_stream('stdin'):
        increment_counter(line=line.rstrip('\n'), counter=counter)
        output(
            formatted_output=format_output(
                # Ensure the order is consistent. Alphabetical order also
                #   more closely matches the behavior or `sort | uniq -c`.
                ordered_counts=sorted(counter.iteritems()),
            )
        )


def increment_counter(line, counter):
    counter[line] += 1


def format_output(ordered_counts):
    return '\n'.join(
        '\t'.join(unicode(x) for x in item) for item in ordered_counts
    )


def output(formatted_output):
    click.clear()
    click.echo(message=formatted_output)
