# backend/routes/skills.py
from flask import Blueprint, request, jsonify
from backend.data.templates import PROJECT_TEMPLATES

skills_bp = Blueprint("skills", __name__)

@skills_bp.route("/api/skills/graph", methods=["POST"])
def generate_skill_graph():
    try:
        user_data = request.json
        current_skills = user_data.get("skills", [])

        nodes = []
        for i, skill in enumerate(current_skills):
            nodes.append({
                "id": skill,
                "label": skill,
                "level": 70 + (i * 5),
                "type": "current"
            })

        edges = []
        for key, project in PROJECT_TEMPLATES.items():
            for new_skill in project["skills_gained"]:
                if new_skill not in current_skills:
                    nodes.append({
                        "id": new_skill,
                        "label": new_skill,
                        "level": 30,
                        "type": "potential"
                    })

                    for lang in project["languages"]:
                        if lang in current_skills:
                            edges.append({
                                "from": lang,
                                "to": new_skill,
                                "project": project["name"]
                            })

        return jsonify({"success": True, "nodes": nodes[:10], "edges": edges[:15]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
