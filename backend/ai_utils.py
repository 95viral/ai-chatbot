import os
from dotenv import load_dotenv
from google import genai
from typing import List, Dict

load_dotenv()

# -------------------------------
# Gemini Client (single instance)
# -------------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)

# -------------------------------
# Public function used by routes
# -------------------------------
def get_ai_response(messages: List[Dict[str, str]]) -> str:
    """
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        ...
    ]
    """

    prompt = build_prompt(messages)

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        
        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            return "Sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error: {str(e)}"


# -------------------------------
# Optional: Document Q&A helper
# -------------------------------
def get_document_response(document_text: str, question: str) -> str:
    prompt = f"""
You are an AI assistant.
Answer ONLY using the document content below.
If the answer is not in the document, say "Not found in document."

DOCUMENT:
{document_text[:8000]}

QUESTION:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        
        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            return "Sorry, I couldn't generate a response for this document."
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error: {str(e)}"



# -------------------------------
# Prompt builder (chat history)
# -------------------------------
def build_prompt(messages):
    prompt = ""

    for msg in messages:
        role = msg.role       # ← FIX
        content = msg.content # ← FIX

        if role == "user":
            prompt += f"User: {content}\n"
        else:
            prompt += f"Assistant: {content}\n"

    return prompt

