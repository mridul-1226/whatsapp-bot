import requests
import tempfile
import imageio_ffmpeg as ffmpeg
import subprocess
import speech_recognition as sr
import os
from urllib.parse import urlparse

class SpeechToTextService:
    def __init__(self, language="en-IN"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def _get_audio_format(self, audio_url: str, content_type: str = None) -> str:
        """Detect audio format from URL or content-type header"""
        if content_type:
            if 'ogg' in content_type:
                return 'ogg'
            elif 'mp3' in content_type or 'mpeg' in content_type:
                return 'mp3'
            elif 'm4a' in content_type or 'mp4' in content_type:
                return 'm4a'
            elif 'wav' in content_type:
                return 'wav'

        parsed_url = urlparse(audio_url)
        path = parsed_url.path.lower()

        if path.endswith('.ogg'):
            return 'ogg'
        elif path.endswith('.mp3'):
            return 'mp3'
        elif path.endswith('.m4a'):
            return 'm4a'
        elif path.endswith('.wav'):
            return 'wav'
        else:
            return 'ogg'

    def transcribe_from_url(self, audio_url: str) -> str:
        try:
            TWILIO_ACCOUNT_SID = os.getenv('TWILIO_SID')
            TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH')
            response = requests.get(audio_url, stream=True, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
            if response.status_code != 200:
                return "Failed to download audio file."

            content_type = response.headers.get('content-type', '')
            audio_format = self._get_audio_format(audio_url, content_type)

            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as temp_in:
                temp_in.write(response.content)
                temp_in_path = temp_in.name

            wav_out_path = temp_in_path.rsplit('.', 1)[0] + ".wav"

            ffmpeg_cmd = [
                ffmpeg.get_ffmpeg_exe(),
                "-i", temp_in_path,
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                wav_out_path
            ]
            subprocess.run(ffmpeg_cmd, check=True)

            os.unlink(temp_in_path)

            with sr.AudioFile(wav_out_path) as source:
                audio_data = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio_data, language=self.language)

            os.unlink(wav_out_path)

            return text

        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError:
            return "Google STT service is unavailable."
        except Exception as e:
            return f"Error: {str(e)}"
