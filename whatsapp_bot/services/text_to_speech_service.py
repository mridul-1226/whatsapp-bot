import os
import platform
from gtts import gTTS
from .cloudinary_service import CloudinaryService

class TTSService:
    def __init__(self, lang="en", slow=False):
        self.lang = lang
        self.slow = slow

    def text_to_speech(self, text, filename="output.mp3"):
        try:
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            tts.save("output.mp3")
            cloud_service = CloudinaryService()
            url = cloud_service.upload_audio("output.mp3")
            print("Uploaded URL:", url)

            return url

        except Exception as e:
            print(f"[TTS Error] {str(e)}")
            return None