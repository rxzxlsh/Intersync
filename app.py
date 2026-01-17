from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

app = FastAPI(title="Intersync Backend")

#front end

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
def resume_build(req: ResumeRequest) -> Dict[str, Any]:
    """
    Step 1 version: no AI yet.
    Just proves frontend -> backend works and returns a structured resume JSON.
    """
    # seeking keywords
    job_text = req.job_description.lower()
    matched = [s for s in req.skills if s.lower() in job_text]

    resume_json = {
        "header": {
            "name": req.name,
            "email": req.email,
            "links": req.links
        },
        "target_role": req.target_role,
        "summary": f"{req.target_role} candidate with skills in {', '.join(req.skills[:6])}.",
        "skills": req.skills,
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

    return {"resume_json": resume_json}

