# backend/routes/projects.py
from flask import Blueprint, request, jsonify
from backend.data.templates import PROJECT_TEMPLATES
from backend.services.resume_utils import calculate_project_relevance

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/api/projects/generate", methods=["POST"])
def generate_projects():
    try:
        user_data = request.json

        scored_projects = []
        for key, project in PROJECT_TEMPLATES.items():
            relevance = calculate_project_relevance(user_data, key, project)
            scored_projects.append({**project, "id": key, "relevance": relevance})

        scored_projects.sort(key=lambda x: x["relevance"], reverse=True)
        top_projects = scored_projects[:3]

        return jsonify({"success": True, "projects": top_projects})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
