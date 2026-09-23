import pygame
import pygame.sndarray
import numpy as np
import cmath
import wave

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

def read():
    with wave.open('voice-telephony-8khz.wav') as wv_obj:
        # samples = wv_obj.readframes(50)
        samples = wv_obj.readframes(wv_obj.getnframes())
        # print(wv_obj.getparams())
        # print(wv_obj.getnframes()/wv_obj.getframerate())
    # int_samples = array.array('h', samples).tolist()
    # padded_samps = int_samples.extend([0]*51744)
    int_samples = np.frombuffer(samples, dtype='h') 
    chunks =  np.array_split(int_samples, np.arange(512, len(int_samples), 512))
    # print(len(chunks))
    # # print(chunks)
    # print((chunks[0]))
    mags = []
    for i in range(len(chunks)):
        mags.append(np.abs(fft(chunks[i])))
    print(mags[0][:256])
    # print(len(mags))
    # print(mags)
    # print(int_samples) 
    # padded_samps = np.pad(int_samples, (0, 51744), mode='constant')
    # print(padded_samps[-1])
    
    # freqs = fft(chunks)
    # nparr = np.array(freqs, dtype=complex)
    # mags = np.abs(freqs)
    # print(mags.size)
    #since real samples produce the same magnitudes in the negative and postive frequency bins
    # we can discard the values in the negative bins and instead multiply the magnitudes in the positive side(excluding the 1st bin(oth bin) and the last Nyquist(256thbin))
    # for now just remving the 0th and the 256th bin and in this code
    positive_sepctrum = [mag[:mag.size//2+1][1:-1]*2 for mag in mags]
    # print(positive_sepctrum[0])
    # positive_sepctrum = mags[:mags.size//2+1]
    # positive_sepctrum[1:-1] *= 2
    freq_res = wv_obj.getframerate()/wv_obj.getnframes()
    actual_freqbins = np.arange(len(positive_sepctrum)) * freq_res

read()

# pygame.mixer.pre_init(frequency = 8000, size= -16, channels = 1)
# pygame.init()
# pygame.mixer.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("black")

#     # RENDER YOUR GAME HERE
#     sound = pygame.mixer.Sound('voice-telephony-8khz.wav')
#     sound.play()
#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     clock.tick(60)  # limits FPS to 60

# pygame.quit()
# pygame.mixer.quit()

# # sound = pygame.mixer.Sound('voice-telephony-8khz.wav')
# # samples = pygame.sndarray.samples(sound)
# # print(samples)