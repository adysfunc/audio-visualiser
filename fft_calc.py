import array
import cmath
import matplotlib.pyplot as plt
import wave
import numpy as np

def fft(samps):
    samplen = len(samps)
    freq = np.zeros(samplen, dtype=complex)
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
    # samples = wv_obj.readframes(10)
    samples = wv_obj.readframes(wv_obj.getnframes())
    print(wv_obj.getparams())
    # print(wv_obj.getnframes()/wv_obj.getframerate())
# int_samples = array.array('h', samples).tolist()
# padded_samps = int_samples.extend([0]*51744)
int_samples = np.frombuffer(samples, dtype='h')
padded_samps = np.pad(int_samples, (0, 51744), mode='constant')
# print(padded_samps[-1])
freqs = fft(padded_samps)
nparr = np.array(freqs, dtype=complex)
mags = np.abs(freqs)
# print(mags.size)
#since real samples produce the same frequencies in the negative and postive
#frequency bins we can discard the values in the negative bins and instead multiply the frequencies in the positive side
positive_sepctrum = mags[:mags.size//2+1]
positive_sepctrum *= 2
freq_res = wv_obj.getframerate()/wv_obj.getnframes()
# actual_freqbins = np.arange(positive_sepctrum.size, positive_sepctrum) * freq_res
actual_freqbins = np.linspace(0, max(positive_sepctrum), positive_sepctrum.size)* freq_res
fig,ax = plt.subplots()
# plt.stem(actual_freqbins, positive_sepctrum,markerfmt='o-')
plt.plot(actual_freqbins, positive_sepctrum)
# plt.xticks(x_axis)
plt.show()