import wave
import array 
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt

# def fft(values):
#     length = len(values)
#     if length == 1:
#         return values
#     else:
#         even_values = fft(values[::2])
#         odd_values = fft(values[1::2])


with wave.open('voice-sample.wav') as wv_obj:
    samples = wv_obj.readframes(500)
    # samples = wv_obj.readframes(wv_obj.getnframes())
    # print(wv_obj.getparams())
    # print(wv_obj.getnframes()/wv_obj.getframerate())
int_samples = array.array('h', samples).tolist()
# samp = np.frombuffer(first_frame, dtype=np.int16)
# print(samp[:5])
fourier = fft(int_samples)
times = np.linspace(0, 6, 500)
fig, ax = plt.subplots()
plt.plot(times, int_samples)
# ax.plot(np.abs(fourier))
plt.show()