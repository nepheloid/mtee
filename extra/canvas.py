#!/usr/bin/env python

"""This lets you draw on an RGB canvas and then dump it in various formats.
Currently PPM and PNG formats are supported.

Use the 'pixel()' method to set and get RGB pixels on the canvas.
Use the '__str__()' method to serialize the canvas.

For testing, try plotting random numbers:

    dd if=/dev/urandom bs=2000 count=1200 | ./canvas.py | display -

AUTHOR

    Noah Spurrier <noah@noah.org>

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


class canvas(object):

    def __init__(self, width=100, height=100):

        '''The image canvas is stored as three separate arrays for
        red, green, and blue. Use the set_canvas() and get_canvas()
        methods to work with the canvas as a single interleved array
        (a list of [R1,G1,B1,R2,G2,B2,R3,G3,B3,...,Rn,Gn,Bn]).
        The pixel() method will set and get pixels on the canvas.
        The __str__() method will render the canvas as a PNG image.
        '''

        self.width = width
        self.height = height
        self.plane_r = [0] * self.width * self.height
        self.plane_g = [0] * self.width * self.height
        self.plane_b = [0] * self.width * self.height
        self.spray_index_max = width * height
        self.spray_index = 0

    def __str__(self):

        # Merge color planes into a flat string.
        flat_canvas = ''.join(map(chr, self.get_canvas()))
        return flat_canvas

    def pixel(self, x, y, r=None, g=None, b=None):

        '''This sets and gets a pixel at the given (x,y) coordinates.
        Use this to both get and set a pixel value.
        If (r,g,b) is given then the pixel is set.
        If (r,g,b) is None then the pixel is not changed.
        In either case the value of the pixel is returned.
        '''

        index = (y * self.width + x)
        if r is not None and g is not None and b is not None:
            self.plane_r[index] = r % 256
            self.plane_g[index] = g % 256
            self.plane_b[index] = b % 256
        return (self.plane_r[index],
                self.plane_g[index],
                self.plane_b[index])

    def spray(self, r, g, b):

        '''This "sprays" color onto the canvas. This follows a raster scan from
        the top,left to the bottom,right. Every time you spray a color the
        spray index in incremented. This is a method useful for streaming
        raster scan bytes onto a canvas. I use it mainly when I want to
        visualize random binary streams. It's useful as a simple way to
        visualize a stream to look for patterns.

        The self.spray_index variable holds the current index as a linear array
        offset, not an x,y offset. This is incremented automatically after each
        call to spray(), so you don't usually need to worry about it. It loops
        around when it gets to the end. '''

        self.plane_r[self.spray_index] = r % 256
        self.plane_g[self.spray_index] = g % 256
        self.plane_b[self.spray_index] = b % 256
        self.spray_index = (self.spray_index + 1) % self.spray_index_max

    def get_canvas(self):

        '''This returns the canvas as a list of sequential R,G,B values.
        The planes for R,G,B are zipped together into a single list.
        '''

        # Merge color planes into a flat string.
        merged_planes = zip(self.plane_r, self.plane_g, self.plane_b)
        canvas = list(I for II in merged_planes for I in II)
        return canvas

    def set_canvas(self, flat_canvas):

        '''This sets the R,G,B planes to the values in the given flat_canvas.
        '''

        assert len(flat_canvas) / 3 == (self.width * self.height), (
            'The flat_canvas is the wrong size.')
        self.plane_r = flat_canvas[0::3]
        self.plane_g = flat_canvas[1::3]
        self.plane_b = flat_canvas[2::3]


class png_canvas(canvas):

    '''Inspired by code by Keegan McAllister:
        https://github.com/kmcallister/blog-misc/blob/master/minpng/minpng.py
    '''

    def __init__(self, width=100, height=100):

        super(png_canvas, self).__init__(width, height)
        self.signature = '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
        # RFC 1950 maximum for window size is 0x8000.
        self.DEFLATE_WINDOW_SIZE = 0x8000

    def __str__(self):

        # Merge color planes into a flat string.
        canvas = ''.join(map(chr, self.get_canvas()))
        # Add NULL filter to the start of each scan-line.
        # This could probably be done in the zip statement above.
        scanlines = ''
        for scanline in self.blocks(canvas, 3 * self.width):
            scanlines += chr(0) + scanline
        return (self.signature
            + self.header()
            + self.chunk('IDAT', self.deflate(scanlines))
            + self.chunk('IEND', ''))

    def bigendian32(self, int32):

        '''This returns a string with the given integer encoded as a 32-bit
        bigendian int. '''

        return (chr((int32 >> 24) & 0xFF)
            + chr((int32 >> 16) & 0xFF)
            + chr((int32 >> 8) & 0xFF)
            + chr(int32 & 0xFF))

    def chunk(self, chunk_type, chunk_data):

        return (self.bigendian32(len(chunk_data))
                + chunk_type
                + chunk_data
                + self.bigendian32(self.crc32(chunk_type + chunk_data)))

    def header(self):

        return self.chunk('IHDR',
                (self.bigendian32(self.width)
                + self.bigendian32(self.height)
                + chr(8)      # bit depth
                + chr(2)      # color type
                + chr(0)      # compression method
                + chr(0)      # filter type
                + chr(0)))    # interlace method

    def blocks(self, biglist, block_size):

        for ii in range(0, len(biglist), block_size):
            yield biglist[ii:ii + block_size]

    def deflate(self, scanlines):

        last_block = False
        zblocks = '\x78\x01'
        for block in self.blocks(scanlines, self.DEFLATE_WINDOW_SIZE):
            block_length = len(block)
            if block_length < self.DEFLATE_WINDOW_SIZE:
                last_block = True
            zblocks += (chr(last_block)
                    + chr(block_length & 0xFF)
                    + chr((block_length >> 8) & 0xFF)
                    + chr((0xFF ^ block_length) & 0xFF)
                    + chr((0xFF ^ (block_length >> 8)) & 0xFF)
                    + block)
        zblocks += self.bigendian32(self.adler32(scanlines))
        return zblocks

    def crc32(self, data):

        crc = 0xFFFFFFFF
        for nn in data:
            crc ^= ord(nn)
            for kk in range(8):
                if crc & 1:
                    crc = 0xEDB88320 ^ (crc >> 1)
                else:
                    crc = crc >> 1
        return crc ^ 0xFFFFFFFF

    def adler32(self, data):

        a = 1
        b = 0
        for dn in data:
            a = (a + ord(dn)) % 0xFFF1
            b = (a + b) % 0xFFF1
        return (b << 16) + a


class ppm_canvas(canvas):

    '''This writes a 24-bit color PPM formatted images (P3 or P6 format).
    This represents an RGB canvas to which you can use the pixel() or spray()
    methods to modify pixels. When done you use the __str__() method to output
    the image as a PPM format.
    dd if=/dev/urandom bs=1000 count=100 | ./ppm-dump | display -
    See http://en.wikipedia.org/wiki/Netpbm_format
    '''

    def __init__(self, width=100, height=100):

        super(ppm_canvas, self).__init__(width, height)
        self.is_ascii = False
        self.imax = 255

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
        for index in range(self.spray_index_max):
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
    canvas = png_canvas(1024, 768)
#    canvas = ppm_canvas(400, 400)
#    canvas.is_ascii = True

####    # Initialize canvas with xor pattern.
####    xcenter = canvas.width / 2
####    ycenter = canvas.height / 2
####    for y in range(0, canvas.height):
####        for x in range(0, canvas.width):
####            dx = x-xcenter
####            dy = y-ycenter
####            val = (dy ^ dx)
####            canvas.draw(x,y,val,val,val)
#            val = (dy ^ dx) % 255
#            canvas.draw(x,y,p.pal_r[val],p.pal_g[val],p.pal_b[val])
#            canvas.spray(pal_r[val],pal_g[val],pal_b[val])

    # Spray bytes from stdin onto canvas.
    for ii in range(1, canvas.spray_index_max):
        try:
            r = ord(sys.stdin.read(1))
            g = ord(sys.stdin.read(1))
            b = ord(sys.stdin.read(1))
            canvas.spray(r, g, b)
        except TypeError, e:
            # read(1) returned empty string.
            break

    # Dump the canvas to stdout.
    sys.stdout.write(str(canvas))

#print """How to detect patterns over an infinite input sequence:
#    1. sequence bytes fill a 2D display buffer.
#    2. when full, display.
#    3. reduce dimensions with subpixel blending.
#    4. each additional byte pushed on the sequence gets averaged.
#    5. Once you have read NN pixels without seeing a pattern you know
#       you need to read at least that number again.
#    ***** ***.* ***..  *.... .....
#"""
