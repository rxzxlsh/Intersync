# backend/app.py
from backend.routes.ai_resume import ai_resume_bp
from flask import Flask
from flask_cors import CORS

from backend.routes.health import health_bp
from backend.routes.projects import projects_bp
from backend.routes.resume import resume_bp
from backend.routes.skills import skills_bp
from backend.routes.ai_resume import ai_resume_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(health_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(ai_resume_bp)


if __name__ == "__main__":
    print("🚀 Intersync Backend Starting...")
    print("📍 Running on http://localhost:5000")
    app.run(debug=True, port=5000)
