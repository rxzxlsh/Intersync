import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY. Put it in backend/.env")

client = genai.Client(api_key=GEMINI_API_KEY)

def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        parts = t.split("```")
        if len(parts) >= 3:
            t = parts[1].strip()
            if t.lower().startswith("json"):
                t = t[4:].strip()
    return t

def tailor_resume_with_gemini(payload: dict) -> dict:
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=json.dumps(payload)
    )
    text = _strip_code_fences(resp.text)
    return json.loads(text)
