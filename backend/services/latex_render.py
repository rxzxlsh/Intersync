# backend/services/latex_render.py

def _escape_latex(s) -> str:
    if s is None:
        return ""
    s = str(s)
    s = s.replace("\\", "\\textbackslash{}")
    s = s.replace("&", "\\&")
    s = s.replace("%", "\\%")
    s = s.replace("$", "\\$")
    s = s.replace("#", "\\#")
    s = s.replace("_", "\\_")
    s = s.replace("{", "\\{")
    s = s.replace("}", "\\}")
    s = s.replace("~", "\\textasciitilde{}")
    s = s.replace("^", "\\textasciicircum{}")
    return s

def _as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]

def _itemize(lines) -> str:
    lines = [l for l in (_escape_latex(l).strip() for l in (lines or [])) if l]
    if not lines:
        return ""
    out = "\\begin{itemize}\\itemsep 0pt\n"
    for l in lines:
        out += f"  \\item {l}\n"
    out += "\\end{itemize}\n"
    return out

def resume_json_to_latex(resume: dict) -> str:
    if not isinstance(resume, dict):
        resume = {}

    header = resume.get("header") or {}
    if not isinstance(header, dict):
        header = {}

    name = _escape_latex(header.get("name") or "Your Name")
    email = _escape_latex(header.get("email") or "")
    links = header.get("links") or []
    if not isinstance(links, list):
        links = []
    links = [_escape_latex(x) for x in links if x]

    headline = _escape_latex(resume.get("headline") or "")

    summary = _as_list(resume.get("summary"))
    skills = resume.get("skills") or {}
    if not isinstance(skills, dict):
        skills = {}

    projects = resume.get("projects") or []
    if not isinstance(projects, list):
        projects = []

    experience = resume.get("experience") or []
    if not isinstance(experience, list):
        experience = []

    contact_parts = [p for p in [email] + links if p]
    contact_line = " | ".join(contact_parts)

    skill_lines = ""
    for section, items in skills.items():
        if not items:
            continue
        items = items if isinstance(items, list) else [items]
        items = [_escape_latex(i) for i in items if i]
        if items:
            skill_lines += f"\\textbf{{{_escape_latex(section)}:}} " + ", ".join(items) + r"\\"
            skill_lines += "\n"

    latex = r"""\documentclass[letterpaper,11pt]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\setlist[itemize]{leftmargin=*,nosep}

\begin{document}

\begin{center}
{\LARGE \textbf{""" + name + r"""}}\\
""" + _escape_latex(contact_line) + r"""\\
\textit{""" + headline + r"""}
\end{center}

\section*{Summary}
""" + (_itemize(summary) or " ") + r"""
\section*{Skills}
""" + (skill_lines or " ") + r"""

\section*{Experience}
"""

    for x in experience:
        if not isinstance(x, dict):
            continue
        title = _escape_latex(x.get("title") or "")
        company = _escape_latex(x.get("company") or "")
        dates = _escape_latex(x.get("dates") or "")
        header_line = "\\textbf{" + (title or "Experience") + "}"
        if company:
            header_line += " --- " + company
        if dates:
            header_line += " \\hfill " + dates
        latex += header_line + "\n\n"
        latex += _itemize(_as_list(x.get("bullets")))
        latex += "\\vspace{2mm}\n"

    latex += "\\section*{Projects}\n"
    for p in projects:
        if not isinstance(p, dict):
            continue
        pname = _escape_latex(p.get("name") or "Project")
        latex += f"\\textbf{{{pname}}}\n\n"
        latex += _itemize(_as_list(p.get("bullets")))
        latex += "\\vspace{2mm}\n"

    latex += r"\end{document}"
    return latex
