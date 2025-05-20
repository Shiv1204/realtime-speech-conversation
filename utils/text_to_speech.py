import os
from google.cloud import texttospeech
import tempfile
from playsound import playsound

def google_cloud_text_to_speech(text, lang="en-US", voice_name="en-US-Wavenet-D"):
    """Convert text to speech using Google Cloud Text-to-Speech and play it."""
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang,
            name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
            out.write(response.audio_content)
            temp_file = out.name
        playsound(temp_file)
        os.remove(temp_file)
    except Exception as e:
        print(f"TTS Error: {e}")