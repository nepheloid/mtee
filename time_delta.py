#!/usr/bin/env python
import time

def time_delta_str (start, end):
    delta = end-start
    if delta < 0:
        delta = -1 * delta
    delta_s = delta % 60
    delta = int(delta)
    delta_m = (delta / 60) % 60
    delta_h = (delta / 3600)
    return '%d hours, %d minutes, %f seconds' % (delta_h, delta_m, delta_s)


start_time = time.time()
end_time = start_time + 12345.6789
print (time_delta_str(start_time, end_time))

