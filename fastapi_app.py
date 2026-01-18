from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from ai_tailor_gemini import tailor_resume_with_gemini


app = FastAPI(title="Intersync Backend")

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

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/resume/build")
async def resume_build(req: ResumeRequest) -> Dict[str, Any]:
    job_text = req.job_description.lower()
    matched = [s for s in req.skills if s.lower() in job_text]

    # Always-works fallback (so demos never break)
    fallback = {
        "header": {"name": req.name, "email": req.email, "links": req.links},
        "target_role": req.target_role,
        "headline": req.target_role,
        "summary": f"{req.target_role} candidate with skills in {', '.join(req.skills[:6])}.",
        "skills": {"Technical Skills": req.skills},
        "projects": [
            {
                "name": p.name,
                "tech": p.tech,
                "bullets": (p.highlights[:3] if p.highlights else [p.description])[:3],
            }
            for p in req.projects
        ],
        "ats_keywords_matched": matched
    }

    payload = {
        "instructions": [
            "You are an expert resume writer and ATS optimizer.",
            "ONLY use the provided skills and projects. DO NOT invent anything.",
            "Tailor to the job description.",
            "Return STRICT JSON only. No markdown, no extra text."
        ],
        "target_role": req.target_role,
        "job_description": req.job_description,
        "candidate": {
            "name": req.name,
            "email": req.email,
            "links": req.links,
            "skills": req.skills,
            "projects": [p.model_dump() for p in req.projects],
        },
        "output_schema": {
            "headline": "string",
            "summary": "string",
            "skills": {"Section Name": ["string"]},
            "projects": [{"name": "string", "bullets": ["string"]}],
            "ats_keywords_matched": ["string"],
            "ats_keywords_missing": ["string"]
        }
    }

    try:
        ai = await tailor_resume_with_gemini(payload)
        return {"resume_json": ai, "used_ai": True}
    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return {
            "resume_json": fallback,
            "used_ai": False,
            "warning": "Gemini failed; fallback returned.",
            "error": str(e)
        }



