import array
import cmath
import matplotlib.pyplot as plt
import wave
import numpy as np

def fft(samps):
    samplen = len(samps)
    freq = [0] * samplen
    # print(samplen)
    if samplen == 1:
        return samps
    else:
        evensamps = fft(samps[::2])
        oddsamps = fft(samps[1::2])
        # freq = array.array('i', [])
        for k in range(samplen//2):
            twiddle = cmath.exp(-2j*cmath.pi*k/samplen)
            freq[k] = evensamps[k] + twiddle*oddsamps[k]
            freq[k+samplen//2] = evensamps[k]- twiddle*oddsamps[k]
        return freq

with wave.open('voice-telephony-8khz.wav') as wv_obj:
    samples = wv_obj.readframes(20)
    # samples = wv_obj.readframes(wv_obj.getnframes())
    print(wv_obj.getparams())
    # print(wv_obj.getnframes()/wv_obj.getframerate())
int_samples = array.array('h', samples).tolist()
freqbins = fft(int_samples)
nparr = np.array(freqbins, dtype=complex)
print(freqbins)
sr = 8000
# N = len(freqbins)
# n = np.arange(N)
# # T = N/sr
# freq = n/T 

fig,ax = plt.subplots()
plt.stem(nparr.real, nparr.imag)
plt.axis('equal')
plt.show()