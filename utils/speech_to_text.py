import speech_recognition as sr

def real_time_speech_to_text():
    """Convert real-time speech to text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening... (Press Ctrl+C to stop)")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError as e:
        return f"Error with the speech recognition service: {e}"