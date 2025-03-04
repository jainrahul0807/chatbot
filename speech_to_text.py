import speech_recognition as sr

def recognize_speech():
    """Converts speech to text using Google Web Speech API."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for up to 5 seconds
            text = recognizer.recognize_google(audio)  # Convert speech to text
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
