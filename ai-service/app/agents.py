"""Small, explainable CareerLens agents suitable for a local college-project demo."""
import re
from collections import defaultdict

ALIASES = {
    "ml": "machine learning", "ai": "artificial intelligence", "js": "javascript",
    "rest api development": "rest api", "restful api": "rest api", "rest api development": "rest api",
    "java programming": "java", "springboot": "spring boot", "postgres": "postgresql",
    "k8s": "kubernetes", "nodejs": "node.js", "reactjs": "react",
}
SKILLS = ["python", "java", "javascript", "typescript", "react", "node.js", "spring boot", "fastapi",
          "sql", "mysql", "postgresql", "mongodb", "docker", "kubernetes", "rest api", "machine learning",
          "artificial intelligence", "data analysis", "pandas", "aws", "azure", "git", "communication",
          "leadership", "problem solving", "project management", "html", "css", "linux", "security", "testing"]

def normalize(s: str) -> str:
    s = re.sub(r"[^a-z0-9.+# ]", " ", s.lower()).strip()
    return ALIASES.get(s, s)

def extract(text: str) -> set[str]:
    t = " " + re.sub(r"[^a-z0-9.+# ]", " ", text.lower()) + " "
    found = set()
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", t):
            found.add(normalize(skill))
    for alias, canonical in ALIASES.items():
        if re.search(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])", t):
            found.add(canonical)
    return found

def analyze(resume_text: str, job_description: str) -> dict:
    # Agents: parsing/extraction, requirement prioritization, gap analysis, planning, projects, interview prep.
    candidate, required = extract(resume_text), extract(job_description)
    matched = sorted(candidate & required)
    missing = sorted(required - candidate)
    # Without confidence evidence, use a review-needed bucket for job skills mentioned in the resume
    # only in weak/aspirational contexts; deterministic MVP leaves this empty and explains evidence limits.
    improvement = []
    match_pct = round(100 * len(matched) / len(required)) if required else 0
    order = sorted(missing, key=lambda x: (x not in {"python", "java", "sql", "rest api", "docker", "fastapi"}, x))
    roadmap = [{"week": i + 1, "stage": "Learn" if i < len(order) else "Build", "skill": skill,
                "topics": [f"{skill.title()} fundamentals", "guided exercises", "apply in a small practical task"],
                "estimated_hours": 5, "priority": "High" if i < 3 else "Medium"} for i, skill in enumerate(order)]
    projects = []
    for skill in order[:4]:
        projects.append({"title": f"{skill.title()} Career Portfolio Project", "difficulty": "Beginner" if len(projects) < 2 else "Intermediate",
                         "estimated_weeks": 2, "skills": [skill],
                         "description": f"Build and document a small role-relevant project that demonstrates {skill} with a working deliverable."})
    if order:
        projects.append({"title": "Integrated Job-Ready Capstone", "difficulty": "Intermediate", "estimated_weeks": 3,
                         "skills": order[:5], "description": "Combine the highest-priority gaps into a deployed, documented portfolio application."})
    questions = []
    for skill in (order[:3] + matched[:2]):
        questions.append({"type": "Technical", "question": f"Explain a practical use of {skill} and how you would approach a common problem with it.",
                          "focus_skill": skill, "expected_topics": [skill, "trade-offs", "testing", "real example"],
                          "sample_answer": f"Describe a concrete example, the approach you chose, key trade-offs, and how you verified the result. Tailor the details to your own experience with {skill}."})
    questions.extend([
        {"type": "Behavioral", "question": "Tell me about a time you learned something quickly to solve a problem.", "focus_skill": "adaptability", "expected_topics": ["situation", "action", "result", "reflection"], "sample_answer": "Use a concise STAR answer: describe the situation, your specific actions, the result, and what you learned."},
        {"type": "Behavioral", "question": "Describe a project setback and how you handled it.", "focus_skill": "problem solving", "expected_topics": ["ownership", "communication", "resolution"], "sample_answer": "Explain the issue, how you communicated it, the steps you took, and the outcome without overstating your role."}
    ])
    return {"match_percentage": match_pct, "matched_skills": matched, "missing_skills": order,
            "improvement_skills": improvement, "candidate_skills": sorted(candidate), "required_skills": sorted(required),
            "skill_priorities": [{"skill": x, "priority": "High" if i < 3 else "Medium"} for i, x in enumerate(order)],
            "roadmap": roadmap, "projects": projects, "interview_questions": questions,
            "notes": ["Skills are identified from text using an editable vocabulary and alias map.", "Match percentage is matched detected skills divided by detected job skills; it is not a hiring probability.", "The demo does not infer proficiency from resume wording. Add evidence-based self-ratings to use the improvement category."]}
