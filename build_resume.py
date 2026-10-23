"""
Generates an ATS-Optimized, Full-Page 1-Page Fresher / 3rd-Year B.Tech Student Resume for Usha Sree Thota
With direct live deployed and repository links, professional summary, and balanced typography.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
import pypdf

OUTPUT_PDF = r"C:\Users\USHA SREE\Desktop\USHA_SREE_THOTA_RESUME.pdf"
PORTFOLIO_RESUME = r"C:\Users\USHA SREE\Desktop\portfolio\resume.pdf"

def build_pdf():
    # Strict 1-page margins calibrated to fill the entire page elegantly
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=22,
        bottomMargin=22
    )

    spacing_factor = 1.35
    font_bump = 0.35

    # Typography
    name_style = ParagraphStyle(
        'Name',
        fontName='Helvetica-Bold',
        fontSize=20 + font_bump,
        leading=23 + font_bump,
        alignment=1, # Center
        textColor=colors.HexColor('#0f172a')
    )
    
    role_style = ParagraphStyle(
        'Role',
        fontName='Helvetica-Bold',
        fontSize=9.5 + font_bump,
        leading=12 + font_bump,
        alignment=1,
        textColor=colors.HexColor('#2563eb'),
        textTransform='uppercase'
    )

    contact_style = ParagraphStyle(
        'Contact',
        fontName='Helvetica',
        fontSize=8.8 + font_bump,
        leading=12 + font_bump,
        alignment=1,
        textColor=colors.HexColor('#334155')
    )

    sec_heading_style = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=10 + font_bump,
        leading=13 + font_bump,
        textColor=colors.HexColor('#0f172a'),
        textTransform='uppercase',
        spaceBefore=4 * spacing_factor,
        spaceAfter=2 * spacing_factor
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.8 + font_bump,
        leading=11.8 + font_bump,
        textColor=colors.HexColor('#1e293b')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8.6 + font_bump,
        leading=11.6 + font_bump,
        leftIndent=11,
        firstLineIndent=-7,
        textColor=colors.HexColor('#1e293b')
    )

    link_sub_style = ParagraphStyle(
        'ProjLinks',
        fontName='Helvetica',
        fontSize=8.2 + font_bump,
        leading=10.8 + font_bump,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # 1. HEADER (Authentic 3rd Year B.Tech Fresher)
    story.append(Paragraph("USHA SREE THOTA", name_style))
    story.append(Spacer(1, 2 * spacing_factor))
    story.append(Paragraph("B.Tech CSE Undergraduate (3rd Year) • Aspiring Software Engineer (Fresher)", role_style))
    story.append(Spacer(1, 3 * spacing_factor))
    
    contact_p1 = "Vijayawada / Guntur, AP &nbsp;•&nbsp; +91 6302018102 &nbsp;•&nbsp; <a href='mailto:thotaushasree09@gmail.com' color='#2563eb'>thotaushasree09@gmail.com</a>"
    contact_p2 = "<b>Portfolio:</b> <a href='https://usha-sree-portfolio.vercel.app' color='#2563eb'><u>usha-sree-portfolio.vercel.app</u></a> &nbsp;•&nbsp; <b>GitHub:</b> <a href='https://github.com/Thota-Usha' color='#2563eb'><u>github.com/Thota-Usha</u></a> &nbsp;•&nbsp; <b>LinkedIn:</b> <a href='https://www.linkedin.com/in/usha-sree-thota-a27a94366/' color='#2563eb'><u>linkedin.com/in/usha-sree-thota</u></a>"
    story.append(Paragraph(contact_p1, contact_style))
    story.append(Spacer(1, 1.5 * spacing_factor))
    story.append(Paragraph(contact_p2, contact_style))
    story.append(Spacer(1, 3 * spacing_factor))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#cbd5e1'), spaceBefore=0, spaceAfter=2 * spacing_factor))

    # 2. PROFESSIONAL SUMMARY
    story.append(Paragraph("PROFESSIONAL SUMMARY", sec_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#0f172a'), spaceBefore=1, spaceAfter=2.5 * spacing_factor))
    summary_text = "Motivated and detail-oriented 3rd-year B.Tech Computer Science undergraduate with a solid foundation in software development, Data Structures, and problem-solving. Hands-on experience developing and deploying responsive web applications, REST APIs with Python and FastAPI, database management (PostgreSQL, MySQL), and big data processing with PySpark. Eager to contribute as an Entry-Level Software Engineer / SDE Intern."
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 3 * spacing_factor))

    # 3. EDUCATION
    story.append(Paragraph("EDUCATION", sec_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#0f172a'), spaceBefore=1, spaceAfter=2.5 * spacing_factor))
    
    edu_table_data = [
        [
            Paragraph("<b>KL University</b>, Vijayawada, Andhra Pradesh", body_style),
            Paragraph("<b>Aug 2024 - May 2028 (Expected)</b>", ParagraphStyle('R1', parent=body_style, alignment=2))
        ],
        [
            Paragraph("Bachelor of Technology (B.Tech) in Computer Science &amp; Engineering (CSE) — <i>3rd Year</i>", ParagraphStyle('Ital', parent=body_style)),
            Paragraph("<b>CGPA: 8.7 / 10.0</b>", ParagraphStyle('R2', parent=body_style, alignment=2))
        ]
    ]
    t_edu = Table(edu_table_data, colWidths=[370, 170])
    t_edu.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
    ]))
    story.append(t_edu)
    story.append(Paragraph("• <b>Relevant Coursework:</b> Data Structures &amp; Algorithms (DSA), Object-Oriented Programming (OOP), Database Management Systems (DBMS), Full-Stack Web Development, Operating Systems, Computer Networks.", bullet_style))
    story.append(Spacer(1, 3 * spacing_factor))

    # 4. TECHNICAL SKILLS
    story.append(Paragraph("TECHNICAL SKILLS", sec_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#0f172a'), spaceBefore=1, spaceAfter=2.5 * spacing_factor))
    
    skills_data = [
        [Paragraph("<b>Programming Languages:</b>", body_style), Paragraph("Python, C, Java, SQL", body_style)],
        [Paragraph("<b>Web Technologies &amp; APIs:</b>", body_style), Paragraph("FastAPI, RESTful APIs, JWT Authentication, HTML5, CSS3, Tailwind CSS", body_style)],
        [Paragraph("<b>Databases &amp; Big Data:</b>", body_style), Paragraph("PostgreSQL (Supabase), MySQL, SQLite, Apache Spark (PySpark), Pandas", body_style)],
        [Paragraph("<b>Developer Tools &amp; Cloud:</b>", body_style), Paragraph("Git, GitHub, VS Code, Postman, Vercel, Railway Cloud, Agile Methodology", body_style)],
        [Paragraph("<b>CS Core Fundamentals:</b>", body_style), Paragraph("Data Structures &amp; Algorithms (DSA), OOP Concepts, Database Design, Problem Solving", body_style)]
    ]
    t_skills = Table(skills_data, colWidths=[140, 400])
    t_skills.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 3 * spacing_factor))

    # 5. PROJECTS (With prominent direct deployed & GitHub URLs right beside titles!)
    story.append(Paragraph("PROJECTS", sec_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#0f172a'), spaceBefore=1, spaceAfter=2.5 * spacing_factor))

    # Project 1: Campus Placement Tracker
    p1_title = [
        [
            Paragraph("<b>Campus Placement &amp; Recruitment Portal</b>", body_style),
            Paragraph("<i>Python, FastAPI, Supabase, Tailwind, JWT</i>", ParagraphStyle('R_p1', parent=body_style, alignment=2, textColor=colors.HexColor('#475569')))
        ]
    ]
    t_p1 = Table(p1_title, colWidths=[330, 210])
    t_p1.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_p1)
    story.append(Paragraph("<b>Live App:</b> <a href='https://placement-tracker-production-2c01.up.railway.app' color='#2563eb'><u>placement-tracker-production-2c01.up.railway.app</u></a> &nbsp;|&nbsp; <b>GitHub:</b> <a href='https://github.com/Thota-Usha/placement-tracker' color='#2563eb'><u>github.com/Thota-Usha/placement-tracker</u></a>", link_sub_style))
    story.append(Paragraph("• Architected an end-to-end recruitment portal for campus drives, handling student records, cutoffs, and multi-tier workflows.", bullet_style))
    story.append(Paragraph("• Implemented automated CGPA validation and a 5-stage recruitment state machine (Applied -> OA -> Interview -> Offered).", bullet_style))
    story.append(Paragraph("• Deployed live on Railway Cloud with Supabase PostgreSQL connection pooling and Swagger API documentation.", bullet_style))
    story.append(Spacer(1, 2.5 * spacing_factor))

    # Project 2: Savory AI Bistro
    p2_title = [
        [
            Paragraph("<b>Savory AI Bistro — Restaurant Platform</b>", body_style),
            Paragraph("<i>Python, REST API, SQLite, HTML5/CSS3, Gemini AI</i>", ParagraphStyle('R_p2', parent=body_style, alignment=2, textColor=colors.HexColor('#475569')))
        ]
    ]
    t_p2 = Table(p2_title, colWidths=[310, 230])
    t_p2.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_p2)
    story.append(Paragraph("<b>GitHub:</b> <a href='https://github.com/Thota-Usha' color='#2563eb'><u>github.com/Thota-Usha</u></a>", link_sub_style))
    story.append(Paragraph("• Developed a full-stack Telugu culinary web application with dynamic menu CRUD, persistent cart state, and table bookings.", bullet_style))
    story.append(Paragraph("• Integrated Gemini AI culinary sommelier alongside an automated Allergen Collision Shield preventing dietary ingredient mismatches.", bullet_style))
    story.append(Paragraph("• Engineered live 5-step order progress tracking and administrative controls with SQLite database storage.", bullet_style))
    story.append(Spacer(1, 2.5 * spacing_factor))

    # Project 3: Big Data Analytics & Cafe App
    p3_title = [
        [
            Paragraph("<b>Food Delivery Big Data Analytics &amp; Cafe System</b>", body_style),
            Paragraph("<i>Python, PySpark, Pandas, MySQL, HTML5/CSS3</i>", ParagraphStyle('R_p3', parent=body_style, alignment=2, textColor=colors.HexColor('#475569')))
        ]
    ]
    t_p3 = Table(p3_title, colWidths=[320, 220])
    t_p3.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_p3)
    story.append(Paragraph("<b>GitHub Repo:</b> <a href='https://github.com/Thota-Usha/food-delivery-big-data-analytics' color='#2563eb'><u>github.com/Thota-Usha/food-delivery-big-data-analytics</u></a>", link_sub_style))
    story.append(Paragraph("• Built an Apache Spark (PySpark) &amp; Pandas analytics pipeline processing delivery records to derive peak-hour logistics trends.", bullet_style))
    story.append(Paragraph("• Developed a companion responsive Cafe Management Web Application with MySQL database for table orders and inventory tracking.", bullet_style))
    story.append(Paragraph("• Visualized key operational metrics and delivery performance insights to optimize turnaround times.", bullet_style))
    story.append(Spacer(1, 3 * spacing_factor))

    # 6. INTERNSHIP & PRACTICAL TRAINING
    story.append(Paragraph("INTERNSHIP &amp; PRACTICAL TRAINING", sec_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#0f172a'), spaceBefore=1, spaceAfter=2.5 * spacing_factor))
    
    exp_header = [
        [
            Paragraph("<b>Software Developer Intern / Trainee</b>", body_style),
            Paragraph("<b>Internship / Training</b>", ParagraphStyle('R_exp', parent=body_style, alignment=2))
        ],
        [
            Paragraph("<i>Software Development &amp; Web Engineering</i>", body_style),
            Paragraph("<i>Remote / Hybrid</i>", ParagraphStyle('R_loc', parent=body_style, alignment=2))
        ]
    ]
    t_exp = Table(exp_header, colWidths=[350, 190])
    t_exp.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_exp)
    story.append(Paragraph("• Assisted in developing, testing, and maintaining responsive web application interfaces using HTML5, CSS3, and Python.", bullet_style))
    story.append(Paragraph("• Collaborated with team peers to debug front-end defects, optimize code structure, and improve page responsiveness.", bullet_style))
    story.append(Paragraph("• Gained hands-on experience in Git version control workflows, code reviews, and Agile software engineering practices.", bullet_style))
    story.append(Spacer(1, 3 * spacing_factor))

    # 7. ACHIEVEMENTS
    story.append(Paragraph("ACHIEVEMENTS &amp; HIGHLIGHTS", sec_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#0f172a'), spaceBefore=1, spaceAfter=2.5 * spacing_factor))
    story.append(Paragraph("• <b>Academic Distinction:</b> Maintaining a consistent <b>8.7 / 10.0 CGPA</b> across 3 years of B.Tech CSE coursework at KL University.", bullet_style))
    story.append(Paragraph("• <b>Live Cloud Deployments:</b> Successfully engineered and deployed live cloud web applications on Railway Cloud and Vercel.", bullet_style))
    story.append(Paragraph("• <b>Technical Engagement:</b> Active participant in coding hackathons, department technical fests, and student developer communities.", bullet_style))

    # Build the document
    doc.build(story)
    
    # Copy to portfolio/resume.pdf
    with open(OUTPUT_PDF, 'rb') as f_in:
        content = f_in.read()
    with open(PORTFOLIO_RESUME, 'wb') as f_out:
        f_out.write(content)
        
    reader = pypdf.PdfReader(OUTPUT_PDF)
    print(f"[SUCCESS] Resume generated at {OUTPUT_PDF} (Total pages: {len(reader.pages)})")

if __name__ == "__main__":
    build_pdf()
