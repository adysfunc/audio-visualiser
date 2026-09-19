import wave

with wave.open('voice-sample.wav') as wv_obj:
    print(wv_obj.readframes(10))
