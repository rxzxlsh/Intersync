# backend/routes/ai_resume.py

from flask import Blueprint, request, jsonify, make_response
from backend.services.ai_tailor_gemini import tailor_resume_with_gemini
from backend.services.latex_render import resume_json_to_latex

ai_resume_bp = Blueprint("ai_resume", __name__)

def build_gemini_payload(target_role: str, job_description: str, candidate: dict) -> dict:
    """
    Build a consistent payload for Gemini so both JSON + .tex routes behave the same.
    """
    return {
        "instructions": [
            # Step 5 prompt improvements
            "You are an expert resume writer, ATS optimizer, and technical recruiter.",
            "ONLY use the provided candidate data. DO NOT invent companies, roles, degrees, dates, or technologies.",
            "Tailor the resume to the target role and the job description.",
            "Extract the most important keywords/skills/tools from the job description and naturally incorporate them where truthful.",
            "Reorder skills, projects, and bullets by relevance to the job description.",
            "Rewrite bullets to be impact-focused and action-oriented. Keep each bullet to 1 line when possible.",
            "If the candidate data includes numbers/metrics, include them. If not, do NOT fabricate metrics.",
            "If a job requirement is missing from candidate data, do not add it—list it in ats_keywords_missing instead.",
            "Return STRICT JSON only that exactly matches output_schema. No markdown, no extra text."
        ],
        "target_role": target_role,
        "job_description": job_description,
        "candidate": candidate,
        "output_schema": {
            "header": {"name": "string", "email": "string", "links": ["string"]},
            "headline": "string",
            "summary": ["string"],
            "skills": {"Section Name": ["string"]},
            "projects": [{"name": "string", "bullets": ["string"]}],
            "experience": [{"title": "string", "company": "string", "bullets": ["string"]}],
            "ats_keywords_matched": ["string"],
            "ats_keywords_missing": ["string"]
        }
    }

@ai_resume_bp.route("/api/ai/resume", methods=["POST"])
def ai_resume():
    data = request.json or {}

    target_role = (data.get("target_role") or "").strip()
    job_description = (data.get("job_description") or "").strip()
    candidate = data.get("candidate") or {}

    if not target_role or not job_description or not isinstance(candidate, dict) or not candidate:
        return jsonify({
            "success": False,
            "error": "Missing target_role, job_description, or candidate"
        }), 400

    payload = build_gemini_payload(target_role, job_description, candidate)

    try:
        resume_json = tailor_resume_with_gemini(payload)

        # ✅ This is what your website needs for copy/download
        latex = resume_json_to_latex(resume_json)

        return jsonify({
            "success": True,
            "used_ai": True,
            "resume_json": resume_json,
            "latex": latex
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "used_ai": False,
            "error": str(e)
        }), 500

@ai_resume_bp.route("/api/ai/resume.tex", methods=["POST"])
def ai_resume_tex():
    """
    Returns a downloadable .tex file.
    Frontend can call this OR just download from the latex returned by /api/ai/resume.
    """
    data = request.json or {}

    target_role = (data.get("target_role") or "").strip()
    job_description = (data.get("job_description") or "").strip()
    candidate = data.get("candidate") or {}

    if not target_role or not job_description or not isinstance(candidate, dict) or not candidate:
        return jsonify({
            "success": False,
            "error": "Missing target_role, job_description, or candidate"
        }), 400

    payload = build_gemini_payload(target_role, job_description, candidate)

    try:
        resume_json = tailor_resume_with_gemini(payload)
        latex = resume_json_to_latex(resume_json)

        response = make_response(latex)
        response.headers["Content-Type"] = "application/x-tex; charset=utf-8"
        response.headers["Content-Disposition"] = "attachment; filename=resume.tex"
        return response

    except Exception as e:
        return jsonify({
            "success": False,
            "used_ai": False,
            "error": str(e)
        }), 500
