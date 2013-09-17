#!/usr/bin/python
# Attempts to implement FIPS-140-2
# Copyright (C) 2009 Kees Cook <kees@outflux.net>
# License: GPLv3
import sys
import unittest


bits = []
index = 0
# eat first 32 bits
toss = ord(sys.stdin.read(1))
toss <<= 8
toss |= ord(sys.stdin.read(1))
toss <<= 8
toss |= ord(sys.stdin.read(1))
toss <<= 8
toss |= ord(sys.stdin.read(1))

for i in range(0, 20000/8):
    c = ord(sys.stdin.read(1))
    for offset in range(0, 8):
        bits.append((c >> 7-offset) & 0x1)


class FIPSTest(unittest.TestCase):

    '''FIPS 140-1'''

    def setUp(self):

        '''Set up prior to each test_* function'''

    def tearDown(self):

        '''Clean up after each test_* function'''

    def validate(self, title, too_low, too_high, value, inclusive=False):

        if inclusive:
            too_low -= 1
            too_high += 1
        format = '%d'
        if isinstance(value, float):
            format = '%0.2f'
        report = "range (%s < %s < %s)" % (format, format, format)
        report = report % (too_low, value, too_high)
        if value <= too_low or value >= too_high:
            rc = False
            report = "%s out of %s!" % (title, report)
        else:
            rc = True
            report = "%s in %s." % (title, report)
        self.assertTrue(rc, report)

    def test_00_monobit(self):

        '''Monobit'''

        ones = 0
        for i in range(0, 20000):
            if bits[i] == 1:
                ones = ones + 1
            elif bits[i] == 0:
                pass
            else:
                raise ValueError("bit %d is not binary (%d)?!" % (i, bits[i]))
        self.validate('ones count', 9725, 10275, ones)

    def test_10_poker(self):

        '''Poker'''

        fi = []
        for i in range(0, 16):
            fi.append(0)
        for i in range(0, 5000):
            value = ((bits[i * 4] << 3)
                     | (bits[i * 4 + 1] << 2)
                     | (bits[i * 4 + 2] << 1)
                     | (bits[i * 4 + 3]))
            fi[value] = fi[value] + 1
        poker = 0.0
        for i in range(0, 16):
            poker = poker + fi[i] * fi[i]
        poker = poker * 16.0 / 5000.0 - 5000.0
        self.validate('poker test result', 2.16, 46.17, poker)

    def test_20_runlength(self):
        '''Run length'''

        class RunCount():

            def __init__(self):
                self.runs = {0: dict(), 1: dict()}
                self.run = 0
                self.prev = None
                self.window_crash = 0
                for i in range(1, 7) + [26]:
                    self.runs[0].setdefault(i, 0)
                    self.runs[1].setdefault(i, 0)

            def _end_run(self):

                if self.run >= 26:
                    self.runs[self.prev][26] += 1
                if self.run >= 6:
                    self.run = 6
                self.runs[self.prev][self.run] += 1
                self.run = 0

            def count(self, binary, prev32):
                prev_window = prev32
                current_window = 0
                self.prev = binary[0]
                self.run = 0
                for i in range(0, len(binary)):
                    current_window = (current_window << 1) & 0xffff
                    current_window |= bits[i]
                    # Test every 32 bits
                    if i > 0 and i % 32 == 0 and current_window == prev_window:
                        self.window_crash = 1
                    if self.prev != binary[i]:
                        self._end_run()
                    self.prev = binary[i]
                    prev_window = (prev_window << 1) & 0xffff
                    prev_window = prev_window & ((current_window >> 31) & 0x1)
                    self.run += 1
                self._end_run()

            def dump(self):
                for n in [0, 1]:
                    for i in range(1, 7) + [26]:
                        print '%d %d: %d' % (n, i, self.runs[n][i])

        runner = RunCount()
        runner.count(bits, toss)
        #runner.dump()
        for n in [0, 1]:
            self.validate('%d run length == 1' % (n), 2343, 2657,
                          runner.runs[n][1], inclusive=True)
            self.validate('%d run length == 2' % (n), 1135, 1365,
                          runner.runs[n][2], inclusive=True)
            self.validate('%d run length == 3' % (n),  452,  708,
                          runner.runs[n][3], inclusive=True)
            self.validate('%d run length == 4' % (n),  251,  373,
                          runner.runs[n][4], inclusive=True)
            self.validate('%d run length == 5' % (n),  111,  201,
                          runner.runs[n][5], inclusive=True)
            self.validate('%d run length >= 6' % (n),  111,  201,
                          runner.runs[n][6], inclusive=True)
            self.validate('%d run length >= 26' % (n),   0,    0,
                          runner.runs[n][26], inclusive=True)
        self.validate('Continuous run', 0,  0,
                      runner.window_crash, inclusive=True)

if __name__ == '__main__':
    unittest.main()
