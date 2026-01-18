# backend/routes/resume.py
from flask import Blueprint, request, jsonify
from backend.data.templates import PROJECT_TEMPLATES
from backend.services.resume_utils import generate_resume_bullets, generate_latex_resume

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/api/resume/generate", methods=["POST"])
def generate_resume():
    try:
        data = request.json
        project_id = data.get("project_id")

        if project_id not in PROJECT_TEMPLATES:
            return jsonify({"success": False, "error": "Project not found"}), 404

        project = PROJECT_TEMPLATES[project_id]
        bullets = generate_resume_bullets(project)

        return jsonify({"success": True, "bullets": bullets})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@resume_bp.route("/api/resume/export-latex", methods=["POST"])
def export_latex():
    try:
        data = request.json
        user_data = data.get("user_data", {})
        project_ids = data.get("project_ids", [])

        projects = [PROJECT_TEMPLATES[pid] for pid in project_ids if pid in PROJECT_TEMPLATES]
        latex_code = generate_latex_resume(user_data, projects)

        return jsonify({"success": True, "latex": latex_code})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

