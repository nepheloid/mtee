MTEE -- Mouse Trap Entropy Engine
=================================

This program produces entropy from a mouse. A mouse event generates several
sources of entropy. The timing and the mouse coordinates could both be used as
sources of entropy. To keep things simple only the coordinates are used.
The primary goal on this program is to be easy to use and understand for
experimentation.

The primary script in this directory is "entropy-source". The "bandwidth.py"
module is used by "entropy-source" to calculate the bits per second of entropy
being generated. The "ev-print.c" program is only needed if you have a buggy
version of Python on a some big-endian processors (PowerPC). It is used to help
correct some constant definitions in "entropy-source". There are also files
under the "extra" directory. These are utilities for converting raw binary data
into images. Sometimes it is useful to look at raw binaries as images as a way
to spot non-random patterns in data. Some of the more interesting file are:

    wl_to_rgb.py ppm_dump.py png_canvas.py canvas.py time_delta.py

If you wish to test the randomness of your entropy then you may want to install
the following tools (these are Debian package names):

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
