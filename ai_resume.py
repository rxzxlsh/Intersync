import os
import json
from typing import List, Optional, Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

load_dotenv()

router = APIRouter(prefix="/resume", tags=["resume"])

# gemini config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# Request models 
class Project(BaseModel):
    name: str
    description: str
    tech: List[str] = Field(default_factory=list)
    highlights: List[str] = Field(default_factory=list)

class ResumeRequest(BaseModel):
    target_role: str
    job_description: str
    name: str

    email: Optional[str] = None
    links: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)


# Fallback (no AI) 
def fallback_resume(req: ResumeRequest) -> Dict[str, Any]:
    return {
        "headline": req.target_role,
        "summary": f"{req.target_role} candidate with skills in {', '.join(req.skills[:6])}.",
        "skills": {"Technical Skills": req.skills},
        "projects": [
            {
                "name": p.name,
                "bullets": (p.highlights[:3] if p.highlights else [p.description])[:3]
            }
            for p in req.projects
        ],
        "note": "Gemini unavailable or failed"
    }


def _strip_code_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1]
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t


# Gemini AI 
async def gemini_tailor(req: ResumeRequest) -> Dict[str, Any]:
    if gemini_client is None:
        return fallback_resume(req)

    prompt = {
        "instructions": [
            "You are an expert resume writer and ATS optimizer.",
            "ONLY use the provided skills and projects.",
            "DO NOT invent experience, metrics, or companies.",
            "Tailor to the job description.",
            "Return STRICT JSON only."
        ],
        "target_role": req.target_role,
        "job_description": req.job_description,
        "candidate": {
            "name": req.name,
            "skills": req.skills,
            "projects": [p.model_dump() for p in req.projects]
        },
        "output_schema": {
            "headline": "string",
            "summary": "string",
            "skills": {"Section Name": ["string"]},
            "projects": [{"name": "string", "bullets": ["string"]}]
        }
    }

    resp = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=json.dumps(prompt)
    )

    text = _strip_code_fences(resp.text or "")
    data = json.loads(text)

    if not isinstance(data, dict) or "summary" not in data or "skills" not in data:
        return fallback_resume(req)

    return data


@router.post("/build")
async def resume_build(req: ResumeRequest):
    try:
        resume_json = await gemini_tailor(req)
        return {"resume_json": resume_json}
    except Exception:
        return {"resume_json": fallback_resume(req), "warning": "Gemini failed"}
