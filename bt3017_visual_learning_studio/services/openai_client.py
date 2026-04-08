import os
from typing import List, Dict

from dotenv import load_dotenv
from google import genai

load_dotenv()


def ask_openai_tutor(
    messages: List[Dict[str, str]],
    topic_context: str,
    page_name: str,
) -> str:
    api_key = (os.getenv("GEMINI_API_KEY") or "").strip()

    if not api_key:
        return "Gemini API key is missing. Check your .env file."

    client = genai.Client(api_key=api_key)

    system_prompt = f"""
You are a BT3017 tutor inside a student learning app.

Your role:
- Help undergraduate computing students understand BT3017 topics.
- Focus only on the topics covered in this app: PCA, Audio Features, and Graph Learning.
- Give explanations that are clear, concise, and beginner-friendly.
- Use intuition first, then add technical detail if helpful.
- If the user asks something outside these topics, say that you are focused on the BT3017 topics in this app.

Current page: {page_name}

Topic context:
{topic_context}

Style rules:
- Be accurate and educational.
- Be concise.
- Use examples when helpful.
- Avoid unnecessary jargon.
"""

    chat_history = []
    for msg in messages:
        role = msg.get("role", "user").upper()
        content = msg.get("content", "")
        chat_history.append(f"{role}: {content}")

    full_prompt = f"""
{system_prompt}

Conversation so far:
{chr(10).join(chat_history)}

Now reply to the user's latest question as the BT3017 tutor.
"""

    # Try models in order
    model_candidates = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
    ]

    last_error = None

    for model_name in model_candidates:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt,
            )
            if response.text:
                return response.text
            return f"The tutor used {model_name}, but no text was returned."
        except Exception as e:
            last_error = e
            continue

    return f"The tutor could not respond right now. Gemini returned: {last_error}"