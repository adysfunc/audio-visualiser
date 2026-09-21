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
        # after spilliting to a single sample
        for k in range(samplen//2):
            twiddle = cmath.exp(-2j*cmath.pi*k/samplen)
            freq[k] = evensamps[k] + twiddle*oddsamps[k]
            freq[k+samplen//2] = evensamps[k]- twiddle*oddsamps[k]
        return freq

with wave.open('voice-telephony-8khz.wav') as wv_obj:
    # samples = wv_obj.readframes(100)
    samples = wv_obj.readframes(wv_obj.getnframes())
    # print(wv_obj.getparams())
    # print(wv_obj.getnframes()/wv_obj.getframerate())
int_samples = array.array('h', samples).tolist()
freqbins = fft(int_samples)
nparr = np.array(freqbins, dtype=complex)
mag = np.abs(nparr)
print(max(mag))
freq_res = wv_obj.getframerate()//wv_obj.getnframes()
x_axis = np.linspace(-max(mag), max(mag), mag.size)
# N = mag.size
# n = np.arange(N)
# # T = N/sr
# freq = n/T 
#TODO: figure out wtf to do after calculating all the freq bins
fig,ax = plt.subplots()
# plt.stem(mag, markerfmt='o-')
plt.plot(x_axis, mag)
plt.axis('equal')
# plt.xticks(x_axis)
plt.show()