"""
AI Resume Chatbot Engine for Usha Sree Thota's Portfolio
Handles recruiter queries about education, skills, projects, and internship readiness.
Supports both Gemini API (if key is set) and a smart built-in knowledge response engine.
"""

import os
import re
import json
import urllib.request
import urllib.error

# Resume Profile Knowledge Base
USHA_PROFILE = {
    "name": "Usha Sree Thota",
    "role": "Computer Science Undergraduate & Full-Stack Developer",
    "college": "KL University (Koneru Lakshmaiah Education Foundation), Vijayawada, Andhra Pradesh",
    "degree": "Bachelor of Technology (B.Tech) in Computer Science & Engineering (CSE)",
    "year": "3rd Year (Aug 2024 – May 2028)",
    "cgpa": "8.7 / 10.0",
    "status": "Actively seeking Full-Time Software Engineering (SDE), Full-Stack Developer, and Backend Developer roles, as well as high-impact engineering opportunities",
    "languages": ["Python", "C", "Java", "JavaScript (ES6+)", "SQL"],
    "web_tech": ["HTML5", "CSS3", "Tailwind CSS", "FastAPI", "REST APIs", "JWT Authentication"],
    "databases_tools": ["PostgreSQL (Supabase)", "MySQL", "SQLite", "Git & GitHub", "PySpark", "Pandas", "VS Code", "Postman"],
    "cs_fundamentals": ["Data Structures & Algorithms (DSA)", "Object-Oriented Programming (OOP)", "Database Management Systems (DBMS)", "Agile Methodology"],
    "projects": [
        {
            "name": "Campus Placement & Recruitment Drive Portal",
            "stack": "Python, FastAPI, Supabase PostgreSQL, Tailwind CSS, JWT Auth",
            "desc": "A production full-stack recruitment portal to verify student CGPA cutoffs automatically, schedule OAs, and track candidate progress across a 5-stage pipeline.",
            "demo": "https://placement-tracker-production-2c01.up.railway.app",
            "repo": "https://github.com/Thota-Usha/placement-tracker"
        },
        {
            "name": "Savory AI Bistro — Full-Stack Restaurant App",
            "stack": "Python, JavaScript, SQLite, HTML5 & CSS3, JWT Auth, Gemini AI",
            "desc": "An intelligent restaurant web app featuring 22+ regional Telugu dishes, real-time cart, live 5-step order tracking, table booking, allergen collision alerts, and an AI culinary sommelier.",
            "repo": "https://github.com/Thota-Usha"
        },
        {
            "name": "Food Delivery Big Data Analytics & Café App",
            "stack": "Python, PySpark, Pandas, MySQL, HTML/CSS/JS",
            "desc": "Engineered an end-to-end data pipeline using Apache Spark to analyze delivery performance metrics alongside a responsive Café Management Web Application.",
            "repo": "https://github.com/Thota-Usha"
        }
    ],
    "experience": "Software Developer Trainee / IT Intern — Assisted in developing responsive internal web tools using HTML, CSS, and JavaScript, debugging application issues, and maintaining code quality.",
    "contact": {
        "email": "thotaushasree09@gmail.com",
        "linkedin": "https://www.linkedin.com/in/usha-sree-thota-a27a94366/",
        "github": "https://github.com/Thota-Usha",
        "location": "Vijayawada / Guntur, Andhra Pradesh, India"
    }
}


def get_ai_response(user_query: str) -> str:
    """
    Answers questions about Usha Sree.
    First checks if GEMINI_API_KEY is available for generative responses.
    Otherwise, uses the smart built-in knowledge response engine.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            return call_gemini(user_query, api_key)
        except Exception as e:
            print(f"Gemini API error, falling back to knowledge engine: {e}")

    return answer_from_knowledge_engine(user_query)


def answer_from_knowledge_engine(query: str) -> str:
    """Smart keyword and semantic intent matcher for recruiter queries."""
    q = query.lower()

    # 1. Greetings
    if re.search(r"\b(hi|hello|hey|namaste|greetings)\b", q):
        return (
            f"Hello! I am Usha Sree's AI Portfolio Assistant. 👋\n\n"
            f"Usha is a B.Tech CSE student at KL University (8.7 CGPA) actively seeking Full-Time Software Engineering (SDE) and Developer roles.\n"
            f"You can ask me about her **Skills**, **Projects**, **Education**, **Experience**, or **Contact details**!"
        )

    # 2. Education & College & CGPA
    if any(k in q for k in ["college", "university", "cgpa", "marks", "education", "degree", "branch", "btech", "b.tech", "year"]):
        return (
            f"🎓 **Education Details:**\n"
            f"• **Degree:** B.Tech in Computer Science & Engineering (CSE)\n"
            f"• **Institution:** KL University (Koneru Lakshmaiah Education Foundation), Vijayawada, AP\n"
            f"• **Current Year:** 3rd Year (Aug 2024 – May 2028)\n"
            f"• **Current CGPA:** **8.7 / 10.0**\n"
            f"• **Key Coursework:** Data Structures & Algorithms, OOPs, DBMS, Web Development."
        )

    # 3. Skills & Technologies
    if any(k in q for k in ["skill", "stack", "tech", "languages", "python", "java", "tools", "c language"]):
        return (
            f"💻 **Technical Skills & Stack:**\n"
            f"• **Languages:** Python, C, Java, JavaScript (ES6+), SQL\n"
            f"• **Web Technologies:** HTML5, CSS3, Tailwind CSS, FastAPI, REST APIs, JWT Auth\n"
            f"• **Databases & Tools:** PostgreSQL (Supabase), MySQL, SQLite, Git & GitHub, PySpark, Pandas, Postman, VS Code\n"
            f"• **Core CS:** DSA, Object-Oriented Programming, Database Design, Agile Methodology."
        )

    # 4. Projects
    if any(k in q for k in ["project", "work", "portfolio", "placement", "restaurant", "bistro", "spark"]):
        return (
            f"🚀 **Featured Projects by Usha Sree:**\n\n"
            f"1. **Campus Placement & Recruitment Drive Portal**\n"
            f"   • *Stack:* Python, FastAPI, Supabase PostgreSQL, Tailwind CSS, JWT Auth\n"
            f"   • *Features:* Automated CGPA cutoff checking, 5-stage recruitment pipeline, live deployment.\n"
            f"   • *Live Demo:* https://placement-tracker-production-2c01.up.railway.app\n\n"
            f"2. **Savory AI Bistro (Full-Stack Restaurant App)**\n"
            f"   • *Stack:* Python, REST API, SQLite, JavaScript, Gemini AI\n"
            f"   • *Features:* 22+ regional dishes, persistent cart, allergen collision safety shield, AI sommelier.\n\n"
            f"3. **Food Delivery Big Data Analytics & Café App**\n"
            f"   • *Stack:* PySpark, Python, Pandas, MySQL, HTML/CSS/JS\n"
            f"   • *Features:* Big data pipeline analyzing delivery metrics + full café management UI."
        )

    # 5. Job Availability & Why Hire Usha
    if any(k in q for k in ["hire", "why", "job", "career", "full-time", "fulltime", "sde", "engineer", "intern", "role", "position"]):
        return (
            f"🌟 **Why Hire Usha Sree as a Software Engineer?**\n\n"
            f"• **High Academic & Practical Acumen:** Maintains an **8.7 CGPA** in CSE at KL University with strong engineering fundamentals.\n"
            f"• **Full-Stack Competence:** Proficient in Python (FastAPI), modern frontend UI (Tailwind CSS, HTML/JS), and Cloud Databases (Supabase PostgreSQL, MySQL).\n"
            f"• **Proven Project Deliverables:** Engineered and deployed production-ready web platforms (Campus Placement Tracker on Railway Cloud, Savory AI Bistro, Big Data PySpark pipeline).\n"
            f"• **Ready for Immediate Impact:** Open to campus recruitment, Full-Time Software Engineer (SDE) roles, and engineering opportunities."
        )

    # 6. Contact & Socials
    if any(k in q for k in ["contact", "email", "reach", "hire", "phone", "linkedin", "github", "location", "address"]):
        return (
            f"📬 **Get in Touch with Usha Sree:**\n"
            f"• **Email:** thotaushasree09@gmail.com\n"
            f"• **LinkedIn:** https://www.linkedin.com/in/usha-sree-thota-a27a94366/\n"
            f"• **GitHub:** https://github.com/Thota-Usha\n"
            f"• **Location:** Vijayawada / Guntur, Andhra Pradesh, India\n\n"
            f"You can also use the contact form at the bottom of this portfolio to send a message directly to her database!"
        )

    # 7. Experience / Work History
    if any(k in q for k in ["experience", "company", "worked", "past", "history"]):
        return (
            f"💼 **Experience:**\n"
            f"• **IT Intern — Software & Web Development:**\n"
            f"  - Assisted in developing and testing responsive internal web tools using HTML5, CSS3, and JavaScript.\n"
            f"  - Supported software debugging activities to resolve application issues.\n"
            f"  - Collaborated with team members following Agile best practices to maintain clean code quality."
        )

    # Default fallback
    return (
        f"Thank you for asking! Usha Sree Thota is a 3rd-year B.Tech CSE student at KL University (8.7 CGPA) with expertise in Python, C, SQL, and Full-Stack Web Development.\n\n"
        f"Would you like to know more about:\n"
        f"1. Her **Projects** (Placement Tracker, Savory AI Bistro, Big Data Analytics)\n"
        f"2. Her **Technical Skills** (Python, FastAPI, Databases, Web)\n"
        f"3. Her **Contact Info** (thotaushasree09@gmail.com)?"
    )


def call_gemini(prompt: str, api_key: str) -> str:
    """Calls Gemini API if an API key is provided"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    system_instruction = (
        f"You are the personal AI Resume Assistant for {USHA_PROFILE['name']}. "
        f"Represent Usha professionally to recruiters. Details: {json.dumps(USHA_PROFILE)}. "
        f"Keep responses professional, concise, enthusiastic, and focused on her technical skills, projects, and readiness for software/web internships."
    )
    
    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"]
