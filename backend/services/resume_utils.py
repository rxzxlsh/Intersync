# backend/services/resume_utils.py
from backend.data.templates import PROJECT_TEMPLATES
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