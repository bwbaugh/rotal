# -*- coding: utf-8 -*-
"""Handles the invocation of the command."""
from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import signal

import click


ASCII_CURSOR_UP = '\033[{num_lines}A'
ASCII_ERASE_TO_END = '\033[K'


@click.command(epilog='Source: https://github.com/bwbaugh/rotal')
@click.version_option()
def main():
    """Get a running count of occurrences from a stream.

    Intended to replace `sort | uniq -c` when the input is a stream.
    """
    # Prevent a broken pipe IOError when used with commands like `head`.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    counter = collections.Counter()
    # Keep track of how many lines we need to move the cursor up.
    num_last_output_lines = 0
    for line in click.get_text_stream('stdin'):
        increment_counter(line=line.rstrip('\n'), counter=counter)
        output(
            formatted_output=format_output_uniqc(
                # Ensure the order is consistent. Alphabetical order also
                #   more closely matches the behavior or `sort | uniq -c`.
                ordered_counts=sorted(counter.iteritems()),
            ),
            num_last_output_lines=num_last_output_lines,
        )
        num_last_output_lines = len(counter)


def increment_counter(line, counter):
    counter[line] += 1


def format_output_uniqc(ordered_counts):
    """Imitate the format of ``uniq -c``."""
    return [
        '{count} {key}'.format(key=key, count=str(count).rjust(4))
        for key, count in ordered_counts
    ]


def output(formatted_output, num_last_output_lines):
    """Output the formatted counts.

    If the terminal is a TTY, then the cursor is moved to update the
    output. When the output is piped to another command, a blank line
    separates a group of output.
    """
    # If the terminal isn't a TTY e.g., when piping the output to
    #   another command, then the `ASCII_ERASE_TO_END` will be
    #   converted to a newline. Prevent this extra newline before the
    #   initial output.
    if num_last_output_lines:
        click.echo(
            # The `ASCII_ERASE_TO_END` being converted to a newline if
            #   the terminal isn't a TTY has the effect of adding a
            #   blank line between groups of output lines. That could
            #   prove to be valuable for some use case, but the
            #   desired behavior when piping the output to another
            #   command hasn't been fully decided on yet.
            message=ASCII_CURSOR_UP.format(
                # Add one since there is an additional newline from the
                #   call to `click.echo()`.
                num_lines=num_last_output_lines + 1,
            ),
        )
    separator = '\n' + ASCII_ERASE_TO_END
    click.echo(message=separator.join(formatted_output))
