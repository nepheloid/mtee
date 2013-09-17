#!/usr/bin/env python

# This sprays bytes from stdin onto a canvas and then
# outputs the result in PPM (portable pixmap file format).
#
# dd if=/dev/urandom bs=1000 count=100 | ./ppm-dump | display -
#
# See http://en.wikipedia.org/wiki/Netpbm_format

"""This lets you draw on an RGB canvas and then dump the canvas as a PPM image.
The PNG is very crude and uncompressed. The code is intended to be small and
simple. It is not fast or efficient.

Use the 'pixel()' method to set and get RGB pixels on the canvas.
Use the '__str__()' method to serialize the canvas to a PNG format.

AUTHOR

    Noah Spurrier <noah@noah.org>
    Inspired by code by Keegan McAllister:
        https://github.com/kmcallister/blog-misc/blob/master/minpng/minpng.py

LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2012, Noah Spurrier
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


class ppm:

    '''This writes a 24-bit color PPM (PNM) formatted images (P3 or P6 format).
    This represents an RGB canvas to which you can use the draw() or spray()
    methods to modify pixels. When done you use the __str__() method to output
    the image as a PPM format. '''

    def __init__(self, width=100, height=100, is_ascii=False):

        self.width = width
        self.height = height
        self.is_ascii = is_ascii
        self.index_max = width*height
        self.plane_r = [0] * self.index_max
        self.plane_g = [0] * self.index_max
        self.plane_b = [0] * self.index_max
        self.imax = 255
        self.index = 0

    def draw(self, x, y, r, g, b):

        index = (y * self.width + x) % self.index_max
        self.plane_r[index] = r % 256
        self.plane_g[index] = g % 256
        self.plane_b[index] = b % 256

    def spray(self, r, g, b):

        self.plane_r[self.index] = r % 256
        self.plane_g[self.index] = g % 256
        self.plane_b[self.index] = b % 256
        self.index = (self.index + 1) % self.index_max

    def __str__(self):

        ppm_str = ''
        if self.is_ascii:
            # ASCII
            ppm_str = ppm_str + "P3"
        else:
            # binary
            ppm_str = ppm_str + "P6"
        ppm_str = ppm_str + "\n"
        ppm_str = ppm_str + str(self.width)
        ppm_str = ppm_str + " "
        ppm_str = ppm_str + str(self.height)
        ppm_str = ppm_str + "\n"
        ppm_str = ppm_str + str(self.imax)
        ppm_str = ppm_str + "\n"
        for index in range(self.index_max):
            r = self.plane_r[index]
            g = self.plane_g[index]
            b = self.plane_b[index]
            if self.is_ascii:
                ppm_str = ppm_str + ('%3d %3d %3d ' % (r, g, b))
                if not ((1 + index) % 6):
                    ppm_str = ppm_str + '\n'
            else:
                ppm_str = ppm_str + chr(r) + chr(g) + chr(b)
        return ppm_str


if __name__ == '__main__':

    import sys
    p = ppm(400, 400)
    #p.is_ascii = True
    #p = ppm(320, 240)
    #p = ppm(640, 480)

####    # Initialize canvas with xor pattern.
####    xcenter = p.width / 2
####    ycenter = p.height / 2
####    for y in range(0, p.height):
####        for x in range(0, p.width):
####            dx = x-xcenter
####            dy = y-ycenter
####            val = (dy ^ dx)
####            p.draw(x,y,val,val,val)
#            val = (dy ^ dx) % 255
#            p.draw(x,y,p.pal_r[val],p.pal_g[val],p.pal_b[val])
#            p.spray(pal_r[val],pal_g[val],pal_b[val])

    # Spray bytes from stdin onto canvas.
    for ii in range(1, p.index_max):
        try:
            r = ord(sys.stdin.read(1))
            g = ord(sys.stdin.read(1))
            b = ord(sys.stdin.read(1))
            p.spray(r, g, b)
        except TypeError, e:
            # read(1) returned empty string.
            break

    # Dump the PPM file to stdout.
    sys.stdout.write(str(p))

#print """How to detect patterns over an infinite input sequence:
#    1. sequence bytes fill a 2D display buffer.
#    2. when full, display.
#    3. reduce dimensions with subpixel blending.
#    4. each additional byte pushed on the sequence gets averaged.
#    5. Once you have read NN pixels without seeing a pattern you know
#       you need to read at least that number again.
#    ***** ***.* ***..  *.... .....
#"""
