import speech_recognition as sr
import sounddevice as sd
import numpy as np

def recognize_speech():
    recognizer = sr.Recognizer()
    samplerate = 44100  # Standard audio rate
    duration = 5  # Recording time in seconds

    print("Listening...")

    try:
        # Record audio using sounddevice
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()

        # Convert to AudioData for recognition
        audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)

        # Recognize speech
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError:
        return "Could not request results, check your connection."

if __name__ == "__main__":
    print(recognize_speech())