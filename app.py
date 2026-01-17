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

"""
Intersync Backend - Flask API
Identity-aligned career development platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Sample project templates database
PROJECT_TEMPLATES = {
    'music': {
        'name': 'Music Data Visualizer',
        'description': 'Interactive visualization of audio data with ML-based genre analysis',
        'languages': ['Python', 'JavaScript'],
        'skills_gained': ['Audio Analysis', 'Data Visualization', 'ML Fundamentals'],
        'difficulty': 'Intermediate',
        'steps': [
            {
                'title': 'Setup audio processing',
                'description': 'Install librosa and process audio files',
                'duration': '2 hours',
                'resources': ['https://librosa.org/doc/latest/index.html']
            },
            {
                'title': 'Create visualizations',
                'description': 'Use matplotlib/plotly for waveforms and spectrograms',
                'duration': '3 hours',
                'resources': ['https://matplotlib.org/stable/gallery/index.html']
            },
            {
                'title': 'Add interactivity',
                'description': 'Build Dash/Streamlit interface',
                'duration': '4 hours',
                'resources': ['https://dash.plotly.com/']
            },
            {
                'title': 'Implement ML',
                'description': 'Train genre classifier with sklearn',
                'duration': '5 hours',
                'resources': ['https://scikit-learn.org/']
            }
        ],
        'neuroplasticity': 'Combines auditory processing with technical skills, strengthening neural pathways between creative and analytical thinking. This cross-domain integration enhances long-term memory retention by 40%.'
    },
    'gaming': {
        'name': 'Gaming Stats Tracker',
        'description': 'Real-time performance analytics dashboard for competitive gaming',
        'languages': ['JavaScript', 'Python'],
        'skills_gained': ['API Integration', 'Real-time Data', 'Dashboard Design'],
        'difficulty': 'Intermediate',
        'steps': [
            {
                'title': 'API research',
                'description': 'Explore gaming APIs (Riot, Steam, Discord)',
                'duration': '2 hours',
                'resources': ['https://developer.riotgames.com/']
            },
            {
                'title': 'Data pipeline',
                'description': 'Fetch and store player statistics',
                'duration': '4 hours',
                'resources': ['https://docs.python-requests.org/']
            },
            {
                'title': 'Build dashboard',
                'description': 'Create React/Vue dashboard with charts',
                'duration': '5 hours',
                'resources': ['https://recharts.org/']
            },
            {
                'title': 'Add analytics',
                'description': 'Performance trends and predictions',
                'duration': '4 hours',
                'resources': ['https://www.chartjs.org/']
            }
        ],
        'neuroplasticity': 'Transforms gaming passion into data literacy, activating reward pathways through personally meaningful projects. Intrinsic motivation increases skill retention by 60%.'
    },
    'robotics': {
        'name': 'Robotics Simulation Platform',
        'description': 'Physics-based robot control and path planning simulator',
        'languages': ['Python', 'C++'],
        'skills_gained': ['Physics Simulation', 'Control Systems', '3D Graphics'],
        'difficulty': 'Advanced',
        'steps': [
            {
                'title': 'Setup PyBullet',
                'description': 'Install physics engine and load basic robots',
                'duration': '3 hours',
                'resources': ['https://pybullet.org/']
            },
            {
                'title': 'Implement controls',
                'description': 'PID controllers for movement',
                'duration': '5 hours',
                'resources': ['https://en.wikipedia.org/wiki/PID_controller']
            },
            {
                'title': 'Path planning',
                'description': 'A* algorithm for navigation',
                'duration': '4 hours',
                'resources': ['https://www.redblobgames.com/pathfinding/a-star/']
            },
            {
                'title': 'Visualization',
                'description': 'Real-time 3D rendering with OpenGL',
                'duration': '4 hours',
                'resources': ['https://learnopengl.com/']
            }
        ],
        'neuroplasticity': 'Engages spatial reasoning and systems thinking, building connections between abstract concepts and physical understanding. Multimodal learning strengthens hippocampal encoding.'
    },
    'photography': {
        'name': 'AI-Powered Photo Organizer',
        'description': 'Automatic photo categorization and enhancement using computer vision',
        'languages': ['Python', 'JavaScript'],
        'skills_gained': ['Computer Vision', 'Deep Learning', 'UI Design'],
        'difficulty': 'Intermediate',
        'steps': [
            {
                'title': 'Setup CV pipeline',
                'description': 'Install OpenCV and load pretrained models',
                'duration': '3 hours',
                'resources': ['https://opencv.org/']
            },
            {
                'title': 'Object detection',
                'description': 'Implement YOLO for scene classification',
                'duration': '5 hours',
                'resources': ['https://pjreddie.com/darknet/yolo/']
            },
            {
                'title': 'Build interface',
                'description': 'Create drag-and-drop photo gallery',
                'duration': '4 hours',
                'resources': ['https://react-dropzone.js.org/']
            },
            {
                'title': 'Auto-enhancement',
                'description': 'Apply filters and adjustments using ML',
                'duration': '4 hours',
                'resources': ['https://pillow.readthedocs.io/']
            }
        ],
        'neuroplasticity': 'Merges artistic vision with technical implementation, activating both visual cortex and logical processing centers. Creative-technical integration promotes cognitive flexibility.'
    },
    'finance': {
        'name': 'Personal Finance Dashboard',
        'description': 'Budget tracking and investment portfolio analyzer',
        'languages': ['Python', 'JavaScript'],
        'skills_gained': ['Data Analysis', 'API Integration', 'Financial Modeling'],
        'difficulty': 'Beginner',
        'steps': [
            {
                'title': 'Data collection',
                'description': 'Connect to financial APIs (Plaid, Alpha Vantage)',
                'duration': '3 hours',
                'resources': ['https://plaid.com/docs/']
            },
            {
                'title': 'Budget analyzer',
                'description': 'Categorize expenses and create insights',
                'duration': '4 hours',
                'resources': ['https://pandas.pydata.org/']
            },
            {
                'title': 'Visualization',
                'description': 'Build interactive charts for spending patterns',
                'duration': '3 hours',
                'resources': ['https://plotly.com/python/']
            },
            {
                'title': 'Investment tracker',
                'description': 'Portfolio performance and predictions',
                'duration': '5 hours',
                'resources': ['https://www.alphavantage.co/']
            }
        ],
        'neuroplasticity': 'Personal financial data creates emotional investment in learning, triggering stronger memory consolidation through relevance and immediate applicability.'
    }
}

RESEARCH_TEMPLATES = [
    {
        'title': 'Neuroplasticity in Skill Acquisition Through Project-Based Learning',
        'difficulty': 'Intermediate',
        'skills': ['Neuroscience', 'Education Theory', 'Data Analysis'],
        'description': 'Investigate how hands-on projects create stronger neural pathways compared to traditional learning methods. Study synaptic strengthening through active engagement.',
        'keywords': ['neuroplasticity', 'learning', 'education']
    },
    {
        'title': 'AI-Driven Personalized Career Path Optimization',
        'difficulty': 'Advanced',
        'skills': ['Machine Learning', 'Career Science', 'NLP'],
        'description': 'Develop algorithms that map individual interests to optimal career trajectories using graph neural networks and reinforcement learning.',
        'keywords': ['ai', 'career', 'optimization', 'machine learning']
    },
    {
        'title': 'Identity-Aligned Motivation in Technical Education',
        'difficulty': 'Intermediate',
        'skills': ['Psychology', 'EdTech', 'Survey Design'],
        'description': 'Study correlation between personal interest integration and learning outcomes in STEM fields. Examine intrinsic vs extrinsic motivation effects.',
        'keywords': ['motivation', 'education', 'psychology']
    },
    {
        'title': 'Computer Vision Applications in Creative Industries',
        'difficulty': 'Advanced',
        'skills': ['Deep Learning', 'Computer Vision', 'Design'],
        'description': 'Explore how CV techniques can augment creative workflows in photography, videography, and digital art.',
        'keywords': ['computer vision', 'creative', 'photography', 'art']
    },
    {
        'title': 'Real-Time Data Processing for Gaming Analytics',
        'difficulty': 'Intermediate',
        'skills': ['Data Engineering', 'Gaming', 'Statistics'],
        'description': 'Build scalable pipelines for processing millions of gaming events per second with low latency.',
        'keywords': ['gaming', 'data', 'real-time']
    },
    {
        'title': 'Robotics Simulation Accuracy and Transfer Learning',
        'difficulty': 'Advanced',
        'skills': ['Robotics', 'Simulation', 'Machine Learning'],
        'description': 'Research sim-to-real transfer techniques to minimize the reality gap in robotic control systems.',
        'keywords': ['robotics', 'simulation', 'machine learning']
    }
]


def calculate_project_relevance(user_data, project_key, project_info):
    """Calculate how relevant a project is to the user (0-100)"""
    score = 50  # Base score
    
    interests = [i.lower() for i in user_data.get('interests', [])]
    skills = [s.lower() for s in user_data.get('skills', [])]
    
    # High bonus if interest matches project category
    if project_key in ' '.join(interests):
        score += 45
    
    # Bonus for relevant skills
    for lang in project_info['languages']:
        if lang.lower() in ' '.join(skills):
            score += 10
    
    # Cap at 100
    return min(score, 100)


def generate_resume_bullets(project):
    """Generate resume bullets for a project"""
    bullets = [
        f"Developed {project['name']}: {project['description'].lower()} using {' and '.join(project['languages'])}",
        f"Implemented {' and '.join(project['skills_gained'][:2])} through {len(project['steps'])}-phase development process",
        f"Built end-to-end solution demonstrating {project['skills_gained'][-1].lower()} with modern development practices"
    ]
    return bullets


def generate_latex_resume(user_data, projects):
    """Generate LaTeX resume code"""
    latex = r"""\documentclass[letterpaper,11pt]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}

\begin{document}

\begin{center}
{\LARGE \textbf{""" + user_data.get('name', 'Your Name') + r"""}}\\
\vspace{2mm}
""" + user_data.get('targetRole', 'Software Developer') + r"""
\end{center}

\section*{Skills}
""" + ', '.join(user_data.get('skills', [])) + r"""

\section*{Projects}
"""
    
    for project in projects:
        bullets = generate_resume_bullets(project)
        latex += f"\n\\textbf{{{project['name']}}} \\\\\n"
        latex += "\\begin{itemize}[leftmargin=*,nosep]\n"
        for bullet in bullets:
            latex += f"    \\item {bullet}\n"
        latex += "\\end{itemize}\n\\vspace{2mm}\n"
    
    latex += r"""
\section*{Interests}
""" + ', '.join(user_data.get('interests', [])) + r"""

\end{document}
"""
    return latex


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/projects/generate', methods=['POST'])
def generate_projects():
    """Generate personalized project suggestions"""
    try:
        user_data = request.json
        
        # Get all projects and score them
        scored_projects = []
        for key, project in PROJECT_TEMPLATES.items():
            relevance = calculate_project_relevance(user_data, key, project)
            scored_projects.append({
                **project,
                'id': key,
                'relevance': relevance
            })
        
        # Sort by relevance and return top 3
        scored_projects.sort(key=lambda x: x['relevance'], reverse=True)
        top_projects = scored_projects[:3]
        
        return jsonify({
            'success': True,
            'projects': top_projects
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/research/generate', methods=['POST'])
def generate_research():
    """Generate personalized research suggestions"""
    try:
        user_data = request.json
        interests = [i.lower() for i in user_data.get('interests', [])]
        skills = [s.lower() for s in user_data.get('skills', [])]
        
        # Score research topics
        scored_research = []
        for topic in RESEARCH_TEMPLATES:
            score = 50
            
            # Check keyword matches
            for keyword in topic['keywords']:
                if any(keyword in interest for interest in interests):
                    score += 15
            
            # Check skill matches
            for skill in topic['skills']:
                if skill.lower() in ' '.join(skills):
                    score += 10
            
            scored_research.append({
                **topic,
                'relevance': min(score, 100)
            })
        
        # Sort and return top 3
        scored_research.sort(key=lambda x: x['relevance'], reverse=True)
        
        return jsonify({
            'success': True,
            'research': scored_research[:3]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/resume/generate', methods=['POST'])
def generate_resume():
    """Generate resume bullets for a project"""
    try:
        data = request.json
        project_id = data.get('project_id')
        
        if project_id not in PROJECT_TEMPLATES:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404
        
        project = PROJECT_TEMPLATES[project_id]
        bullets = generate_resume_bullets(project)
        
        return jsonify({
            'success': True,
            'bullets': bullets
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/resume/export-latex', methods=['POST'])
def export_latex():
    """Export full resume as LaTeX"""
    try:
        data = request.json
        user_data = data.get('user_data', {})
        project_ids = data.get('project_ids', [])
        
        # Get selected projects
        projects = [PROJECT_TEMPLATES[pid] for pid in project_ids if pid in PROJECT_TEMPLATES]
        
        # Generate LaTeX
        latex_code = generate_latex_resume(user_data, projects)
        
        return jsonify({
            'success': True,
            'latex': latex_code
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/skills/graph', methods=['POST'])
def generate_skill_graph():
    """Generate skill graph data for visualization"""
    try:
        user_data = request.json
        current_skills = user_data.get('skills', [])
        
        # Create nodes for current skills
        nodes = []
        for i, skill in enumerate(current_skills):
            nodes.append({
                'id': skill,
                'label': skill,
                'level': 70 + (i * 5),  # Simulated skill level
                'type': 'current'
            })
        
        # Add potential new skills from projects
        edges = []
        for key, project in PROJECT_TEMPLATES.items():
            for new_skill in project['skills_gained']:
                if new_skill not in current_skills:
                    nodes.append({
                        'id': new_skill,
                        'label': new_skill,
                        'level': 30,
                        'type': 'potential'
                    })
                    
                    # Create edges from current skills to new skills
                    for lang in project['languages']:
                        if lang in current_skills:
                            edges.append({
                                'from': lang,
                                'to': new_skill,
                                'project': project['name']
                            })
        
        return jsonify({
            'success': True,
            'nodes': nodes[:10],  # Limit to 10 nodes for clarity
            'edges': edges[:15]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Intersync Backend Starting...")
    print("📍 Running on http://localhost:5000")
    print("🔗 API Endpoints:")
    print("   - POST /api/projects/generate")
    print("   - POST /api/research/generate")
    print("   - POST /api/resume/generate")
    print("   - POST /api/resume/export-latex")
    print("   - POST /api/skills/graph")
    app.run(debug=True, port=5000)
