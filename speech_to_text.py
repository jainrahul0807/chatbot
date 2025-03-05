import sounddevice as sd
import numpy as np
import speech_recognition as sr

def recognize_speech():
    samplerate = 44100  # Sampling rate
    duration = 5  # seconds
    print("Recording...")

    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to finish
    print("Recording done!")

    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized Speech:", text)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results"
