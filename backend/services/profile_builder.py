def build_profile(payload: dict) -> dict:
    target_role = payload.get("targetRole", "")

    role_keywords = {
        "Backend Developer": ["APIs", "REST", "SQL", "Docker", "Git", "authentication"],
        "Frontend Developer": ["JavaScript", "UI", "accessibility", "responsive design"],
        "Data Analyst": ["SQL", "dashboards", "metrics", "A/B testing"],
        "ML Intern": ["Python", "datasets", "evaluation", "pipelines"],
    }

    return {
        "targetRole": target_role,
        "keywords": role_keywords.get(target_role, []),
        "user": payload.get("user", {}),
        "questionnaire": payload.get("questionnaire", {}),
        "constraints": {"onePage": True, "format": "ATS"},
    }
