#!/usr/bin/env python
# vim:set ft=python fileencoding=utf-8 sr et ts=4 sw=4 : See help 'modeline'
"""Bandwidth calculator.

AUTHOR

    Noah Spurrier <noah@noah.org>

LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2013, Noah Spurrier
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

VERSION

    Version 1
"""

import os
import sys
import time


class bandwidth:

    def __init__(self):

        self.byte_count_history = [[0.0, 0]]
        self.byte_count_history_max_secs = 15 * 3600
        self.bin_length_secs = 10.0

    def __str__(self):

        ss = ''
        ss += '1 minute bandwidth: %f\n' % self.bandwidth_covering(60.0)
        ss += '5 minute bandwidth: %f\n' % self.bandwidth_covering(300.0)
        ss += 'history length: %d\n' % len(self.byte_count_history)
        ss += 'log of update times and byte counts:\n'
        ss += '    ' + str(self.byte_count_history)
        return ss

    def update(self, byte_count):

        now_time = time.time()
        # Add byte_count to history. Aggregate into bins of bin_length_secs.
        if (len(self.byte_count_history) > 0 and
                now_time - self.byte_count_history[-1][0] <
                self.bin_length_secs):
            self.byte_count_history[-1][1] += byte_count
        else:
            self.byte_count_history.append([now_time, byte_count])
        # Drop byte_counts that are older than byte_count_history_max_secs.
        # FIXME: Yes, I know lists are inefficient as dequeues.
        while (len(self.byte_count_history) > 0 and
                (now_time - self.byte_count_history[0][0]) >
                self.byte_count_history_max_secs):
            self.byte_count_history.pop(0)

    def bandwidth_covering(self, timespan_secs):

        if len(self.byte_count_history) < 1:
            return 0.0
        now_time = time.time()
        # Find the point in history newer than timespan_secs.
        for ii in range(len(self.byte_count_history)):
            if now_time - self.byte_count_history[ii][0] <= timespan_secs:
                break
        # Calculate total_time from point in history previously found.
        time_total = now_time - self.byte_count_history[ii][0]
        # Get the sum of byte counts starting from the point previously found.
        byte_total = 0
        for ii in range(ii, len(self.byte_count_history)):
            byte_total += self.byte_count_history[ii][1]
        return byte_total / time_total


if __name__ == '__main__':

    print('Initializing bandwidth counts...')
    bw = bandwidth()

    for ii in range(60):
        bw.update(1)
        print(bw)
        time.sleep(1)
    for ii in range(60):
        bw.update(2)
        print(bw)
        time.sleep(1)
    for ii in range(10000):
        bw.update(1)
        print(bw)
        time.sleep(1)
