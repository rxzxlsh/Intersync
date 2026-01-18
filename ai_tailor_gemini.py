import os, json
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1].strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t

async def tailor_resume_with_gemini(payload: dict) -> dict:
    if client is None:
        raise RuntimeError("Missing GEMINI_API_KEY in .env")

    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=json.dumps(payload)
    )

    text = _strip_code_fences(resp.text)
    return json.loads(text)
