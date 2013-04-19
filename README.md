MTEE -- Mouse Trap Entropy Engine
=================================

Mouse Trap Entropy Engine

This application produces entropy from a mouse.

The key script in this directory is "entropy-source". Most of the rest of the
files are noise. Some of the other more interesting file are:

    wl_to_rgb.py ppm_dump.py png_canvas.py canvas.py time_delta.py

Most of these have nothing to do with randomness or entropy. They are small
utilities for converting raw binary data to images.

A mouse event generates several sources of entropy. The timing and the mouse
coordinates could both be used as sources of entropy. At the moment I only use
the coordinates. This could easily be extended to absolute time, delta time, X,
and Y coordinates for much more entropy. My goal here was to create something
that is easy to understand, so I don't use all sources of entropy available to
us. My goal was to make a fairly complete script that is also easy to
understand and follow. Optimizations may be added later if they don't detract
from clarity.

You may want to install the following tools for testing randomness:
    apt-get install rng-tools ent dieharder

-- 
Noah Spurrier <noah@noah.org>

LICENSE

    This is free and open software. You may do anything with it.

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2013, Noah Spurrier <noah@noah.org>
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
