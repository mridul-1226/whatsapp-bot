import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(user_message: str, chat_history: list = None) -> str:
    """
    user_message: latest user input (str)
    chat_history: list of dicts [{'role': 'user'/'assistant', 'content': str}, ...]
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        system_prompt = (
            "You are StudyBuddy, an AI tutor. "
            "- Answer concisely (max 2 sentences). "
            "- Do not mention you are an AI or how you generate answers. "
            "- Always keep focus on educational explanation with short examples. "
            "- If the question is unclear, politely ask for clarification."
            "- Try to reply in hinglish only."
        )
        messages = []
        if chat_history and len(chat_history) > 0:
            for msg in chat_history:
                messages.append({
                    "role": msg["role"],
                    "parts": [msg["content"]]
                })
            messages.append({"role": "user", "parts": [user_message]})
        else:
            messages.append({
                "role": "user",
                "parts": [f"{system_prompt}\n{user_message}"]
            })

        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry, I couldn’t generate an answer."
