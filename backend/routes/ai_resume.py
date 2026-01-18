# backend/routes/ai_resume.py

import os
from flask import Blueprint, request, jsonify, make_response

from backend.services.ai_tailor_gemini import tailor_resume_with_gemini
from backend.services.latex_render import resume_json_to_latex

ai_resume_bp = Blueprint("ai_resume", __name__)


def build_gemini_payload(target_role: str, job_description: str, candidate: dict) -> dict:
    return {
        "instructions": [
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


def build_demo_resume(target_role: str, candidate: dict) -> dict:
    """Deterministic fallback: always works even without GEMINI_API_KEY."""
    return {
        "header": {
            "name": candidate.get("name", "Candidate Name"),
            "email": candidate.get("email", ""),
            "links": candidate.get("links", []) if isinstance(candidate.get("links", []), list) else []
        },
        "headline": target_role,
        "summary": [
            f"{target_role} candidate with hands-on project experience and strong fundamentals."
        ],
        "skills": {
            "Technical Skills": candidate.get("skills", []) if isinstance(candidate.get("skills", []), list) else []
        },
        "projects": candidate.get("projects", []) if isinstance(candidate.get("projects", []), list) else [],
        "experience": candidate.get("experience", []) if isinstance(candidate.get("experience", []), list) else [],
        "ats_keywords_matched": [],
        "ats_keywords_missing": []
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

    # ✅ Demo fallback toggle
    ai_enabled = os.getenv("AI_ENABLED", "true").lower() == "true"

    # If no key, auto-disable AI (so teammates don't crash)
    if not os.getenv("GEMINI_API_KEY"):
        ai_enabled = False

    if not ai_enabled:
        resume_json = build_demo_resume(target_role, candidate)
        latex = resume_json_to_latex(resume_json)
        return jsonify({
            "success": True,
            "used_ai": False,
            "resume_json": resume_json,
            "latex": latex
        })

    # AI path
    payload = build_gemini_payload(target_role, job_description, candidate)

    try:
        resume_json = tailor_resume_with_gemini(payload)
        latex = resume_json_to_latex(resume_json)
        return jsonify({
            "success": True,
            "used_ai": True,
            "resume_json": resume_json,
            "latex": latex
        })
    except Exception as e:
        # If AI fails, fallback instead of breaking demo
        resume_json = build_demo_resume(target_role, candidate)
        latex = resume_json_to_latex(resume_json)
        return jsonify({
            "success": True,
            "used_ai": False,
            "warning": "Gemini failed; fallback used.",
            "error": str(e),
            "resume_json": resume_json,
            "latex": latex
        })


@ai_resume_bp.route("/api/ai/resume.tex", methods=["POST"])
def ai_resume_tex():
    data = request.json or {}

    target_role = (data.get("target_role") or "").strip()
    job_description = (data.get("job_description") or "").strip()
    candidate = data.get("candidate") or {}

    if not target_role or not job_description or not isinstance(candidate, dict) or not candidate:
        return jsonify({
            "success": False,
            "error": "Missing target_role, job_description, or candidate"
        }), 400

    ai_enabled = os.getenv("AI_ENABLED", "true").lower() == "true"
    if not os.getenv("GEMINI_API_KEY"):
        ai_enabled = False

    try:
        if ai_enabled:
            payload = build_gemini_payload(target_role, job_description, candidate)
            resume_json = tailor_resume_with_gemini(payload)
        else:
            resume_json = build_demo_resume(target_role, candidate)

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
