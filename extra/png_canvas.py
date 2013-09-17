
"""This lets you draw on an RGB canvas and then dump the canvas as a PNG image.
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


class png_canvas:

    def __init__(self, width=100, height=100):

        '''The image canvas is stored as three separate arrays for
        red, green, and blue. Use the set_canvas() and get_canvas()
        methods to work with the canvas as a single interleved array.
        The pixel() method will set and get pixels on the canvas.
        The __str__() method will render the canvas as a PNG image.
        '''

        self.width = width
        self.height = height
        self.plane_r = [0] * self.width * self.height
        self.plane_g = [0] * self.width * self.height
        self.plane_b = [0] * self.width * self.height
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
        return(self.signature
               + self.header()
               + self.chunk('IDAT', self.deflate(scanlines))
               + self.chunk('IEND', ''))

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

    def get_canvas(self):

        '''This returns the canvas as a list of sequential R,G,B values.
        The planes for R,G,B are zipped together into a single list.
        '''

        # Merge color planes into a flat string.
        merged_planes = zip(self.plane_r, self.plane_g, self.plane_b)
        canvas = list(I for II in merged_planes for I in II)
        return canvas

    def set_canvas(self, canvas):

        '''This sets the R,G,B color planes to the values in the given canvas.
        '''

        assert len(canvas) / 3 == (self.width * self.height), (
            'The canvas is the wrong size.')
        self.plane_r = canvas[0::3]
        self.plane_g = canvas[1::3]
        self.plane_b = canvas[2::3]

    def bigendian32(self, int32):

        '''This returns a string with the given integer encoded as a 32-bit
        bigendian int. '''

        return(chr((int32 >> 24) & 0xFF)
               + chr((int32 >> 16) & 0xFF)
               + chr((int32 >> 8) & 0xFF)
               + chr(int32 & 0xFF))

    def chunk(self, chunk_type, chunk_data):

        return(self.bigendian32(len(chunk_data))
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
