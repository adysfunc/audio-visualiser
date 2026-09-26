import pygame
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
    
        # after spilliting to a single sample
        # the FFT calculation 
        for k in range(samplen//2):
            twiddle = cmath.exp(-2j*cmath.pi*k/samplen)
            freq[k] = evensamps[k] + twiddle*oddsamps[k]
            freq[k+samplen//2] = evensamps[k]- twiddle*oddsamps[k]
        return freq

def read():
    with wave.open('voice-telephony-8khz.wav') as wv_obj:
        FRAMERATE = wv_obj.getframerate()
        samples = wv_obj.readframes(wv_obj.getnframes())
     
     #convert raw bytes to signed integers then split them into arrays of 512 samples(used the array module previously)   
    int_samples = np.frombuffer(samples, dtype='h') 
    chunks =  np.array_split(int_samples, np.arange(512, len(int_samples), 512))
    # print(len(chunks))
    # # print(chunks)
    # print((chunks[0]))
    
    mags = []
    for i in range(len(chunks)):
        mags.append(np.abs(fft(chunks[i])))
    
    #since real samples produce the same magnitudes in the negative and postive frequency bins
    # we can discard the values in the negative bins and instead multiply the magnitudes in the positive side(excluding the 1st bin(oth bin) and the last Nyquist(256thbin))
    # for now just remving the 0th and the 256th bin and in this code
    positive_spectrum = [mag[:mag.size//2+1][1:-1]*2 for mag in mags]
     
    freq_res = FRAMERATE/512
    #no need of frequency bins to plot only did it to understand the FFT
    # freq_bins = [np.arange(len(values))* freq_res for values in positive_spectrum]
    return positive_spectrum, freq_res
    
points, frequency_resolution = read()
delta = frequency_resolution/60
pygame.mixer.pre_init(frequency = 8000, size= -16, channels = 1, buffer = 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
#used the msuic module instead of sound
pygame.mixer.music.load('voice-telephony-8khz.wav')

count = 0
while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # bin_to_draw = points[0]
    # to choose which chunk to show
    count += delta
    frame_to_draw = points[int(count)]
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    for i in range(len(frame_to_draw)):
        #get the max value from the frame samples
        maxmag = max(frame_to_draw)
        bar_width = screen.get_width()/len(frame_to_draw)
        #for every sample/point divide bt the max value and multiply by the screen width in order to fit them in the screen
        height = frame_to_draw[i]/maxmag * 720
        pygame.draw.rect(screen, (255,255,255), (i*bar_width, 720-height, bar_width, height))

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    
    clock.tick(60)  # limits FPS to 60
    pygame.display.update()

pygame.quit()
pygame.mixer.quit()
