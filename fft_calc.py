import array
import cmath

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

samps = [11, 12, 13, 14, 15, 16, 17, 18]
print(fft(samps))