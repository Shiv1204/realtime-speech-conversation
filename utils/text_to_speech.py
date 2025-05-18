from gtts import gTTS
from playsound import playsound
import os

def real_time_text_to_speech(text):
    """Convert text to speech and play it in real-time."""
    try:
        tts = gTTS(text=text, lang='en')
        output_file = "audio/response.mp3"
        tts.save(output_file)
        playsound(output_file)
        os.remove(output_file)  # Clean up the temporary file
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")