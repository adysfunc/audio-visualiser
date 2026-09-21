import wave
import array 
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt
import cmath

def fft(samps):
    samplen = len(samps)
    freq = np.zeros(samplen, dtype=complex)
    # print(samplen)
    if samplen == 1:
        return samps
    else:
        evensamps = fft(samps[::2])
        oddsamps = fft(samps[1::2])
        # after spilliting to a single sample
        for k in range(samplen//2):
            twiddle = cmath.exp(-2j*cmath.pi*k/samplen)
            freq[k] = evensamps[k] + twiddle*oddsamps[k]
            freq[k+samplen//2] = evensamps[k]- twiddle*oddsamps[k]
        return freq

with wave.open('voice-telephony-8khz.wav') as wv_obj:
    # samples = wv_obj.readframes(10)
    samples = wv_obj.readframes(wv_obj.getnframes())
    print(wv_obj.getparams())
    # print(wv_obj.getnframes()/wv_obj.getframerate())
# int_samples = array.array('h', samples).tolist()
int_samples = np.frombuffer(samples, dtype='h')
print(int_samples.size)
padded_samps = np.pad(int_samples, (0, 51744), mode='constant')
print(padded_samps.size)
# print(np_samples)
freqs = fft(padded_samps)
print(type(freqs))
# print(len(freqs))
mags = np.abs(freqs)
for k in range(1, len(mags)//2):
    print(k, mags[k], mags[len(mags)-k])