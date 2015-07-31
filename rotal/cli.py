# -*- coding: utf-8 -*-
"""Handles the invocation of the command."""
from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import signal

import click


@click.command()
def main():
    """Get a running count of occurrences from a stream.

    Intended to replace `sort | uniq -c` when the input is a stream.
    """
    # Prevent a broken pipe IOError when used with commands like `head`.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    counter = collections.Counter()
    for line in click.get_text_stream('stdin'):
        increment_counter(line=line.rstrip('\n'), counter=counter)
        output(
            formatted_output=format_output_uniqc(
                # Ensure the order is consistent. Alphabetical order also
                #   more closely matches the behavior or `sort | uniq -c`.
                ordered_counts=sorted(counter.iteritems()),
            )
        )


def increment_counter(line, counter):
    counter[line] += 1


def format_output_uniqc(ordered_counts):
    """Imitate the format of ``uniq -c``."""
    return '\n'.join(
        '{count} {key}'.format(key=key, count=str(count).rjust(4))
        for key, count in ordered_counts
    )


def output(formatted_output):
    click.clear()
    click.echo(message=formatted_output)
