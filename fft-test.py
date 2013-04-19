#!/usr/bin/env python

import scipy
import scipy.fftpack
import pylab
import numpy
from scipy import pi

####t = scipy.linspace(0,120,4000)
#####acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t) + 2*scipy.random.random(len(t))
####acc = lambda t: 10*scipy.sin(2*pi*10.0*t) + 5*scipy.sin(2*pi*5.0*t)
####signal = acc(t)
####FFT = abs(scipy.fft(signal))
####freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
####pylab.subplot(211)
####pylab.plot(t, signal)
####pylab.subplot(212)
####pylab.plot(freqs,20*scipy.log10(FFT))
####pylab.show()

from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange

def plotSpectrum(y,Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]
    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = arange(0,1,Ts) # time vector

ff = 5;   # frequency of the signal
y = sin(2*pi*ff*t)

subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
plotSpectrum(y,Fs)
show()
