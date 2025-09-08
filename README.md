# WhatsApp Study Bot

This is a Django-based WhatsApp bot that uses Twilio to send AI-generated responses for WhatsApp messages. The bot can respond with both text and audio messages.

## Features

- **AI-Powered Responses:** Integrates with a generative AI model to provide intelligent and context-aware responses.
- **Text and Audio:** Can send responses in both text and audio formats.
- **Twilio Integration:** Uses Twilio's WhatsApp API to receive and send messages.
- **Cloudinary for Media:** Uses Cloudinary to store and deliver audio files.

## Technologies Used

- Django
- Django Rest Framework
- Google Generative AI
- Twilio
- Cloudinary
- gTTS (Google Text-to-Speech)
- SpeechRecognition

## AI Model Details

- **Chat History:** The bot stores user-specific chat histories on the server to maintain context across messages, allowing for more personalized and coherent responses.
- **Availability:** The AI responses are generated in real-time, with text and audio formats available for all supported message types.

## Project Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:mridul-1226/whatsapp-bot.git
   cd study_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following variables:

   ```
   TWILIO_ACCOUNT_SID=
   TWILIO_AUTH_TOKEN=
   GEMINI_API_KEY=
   CLOUDINARY_CLOUD_NAME=
   CLOUDINARY_API_KEY=
   CLOUDINARY_API_SECRET=
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Configure Twilio Webhook:**
   - Start ngrok to expose your local server to the internet:
     ```bash
     ngrok http 8000
     ```
   - In your Twilio account, configure the WhatsApp sandbox webhook to point to `https://<your-ngrok-url>/whatsapp/receive/`.

## API Endpoints

- `/whatsapp/receive/`: The main endpoint for receiving WhatsApp messages via Twilio webhook.

---
Made with ❤️
