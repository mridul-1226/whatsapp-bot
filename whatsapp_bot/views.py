# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from .services import gemini_service, speech_to_text_service as stt, text_to_speech_service as tts

user_chat_histories = {}


class WhatsAppWebhook(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Handle incoming WhatsApp messages from Twilio
        """
        try:
            from_number = request.data.get("From")
            body = request.data.get("Body")
            media_url = request.data.get("MediaUrl0")
            media_type = request.data.get("MediaContentType0")
            isAudio = False
            data = request.data
            print(data)

            if not body and not media_url:
                return Response({"error": "No message content"}, status=status.HTTP_400_BAD_REQUEST)
            elif not body:
                if not media_type or not media_type.startswith("audio"):
                    return Response({"message": f"Unsupported media type: {media_type}"}, status=status.HTTP_400_BAD_REQUEST)
                stt_service = stt.SpeechToTextService()
                body = stt_service.transcribe_from_url(audio_url=media_url)
                isAudio = True

            user_id = from_number

            chat_history = user_chat_histories.get(user_id, [])

            reply_text = gemini_service.get_gemini_response(body, chat_history)
            print(reply_text)

            if isAudio:
                hindi_tts = tts.TTSService(lang="hi")
                url = hindi_tts.text_to_speech(reply_text)

            print(url)

            chat_history.append({"role": "user", "content": body})
            chat_history.append({"role": "assistant", "content": reply_text})
            user_chat_histories[user_id] = chat_history
            print(f"reply: {reply_text}\n")

            resp = MessagingResponse()
            msg = resp.message(reply_text)
            if isAudio:
                msg.media(url)

            account_sid = os.getenv('TWILIO_SID')
            auth_token = os.getenv('TWILIO_AUTH')
            client = Client(account_sid, auth_token)

            client.messages.create(
                from_="whatsapp:+14155238886",
                to=from_number,
                body=reply_text,
                media_url=[url] if isAudio else None
            )

            return Response(str(resp), content_type="application/xml", status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)

    def get(self, request, *args, **kwargs):
        return Response({"message": "WhatsApp Webhook Working ✅"})
