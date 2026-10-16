"""
FastAPI Backend Application for Usha Sree Thota's Portfolio
Provides:
  - Contact Form submission API & message persistence
  - Live Visitor / Analytics Counter
  - AI Resume Chatbot API
  - Interactive Swagger Docs at /docs
  - Direct static frontend serving
"""

import os
from datetime import datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import init_db, get_db, ContactMessage, SiteStat, VisitorLog
from chatbot import get_ai_response

# Initialize SQLite database
init_db()

app = FastAPI(
    title="Usha Sree Thota — Portfolio & Resume API",
    description="Backend API powering Usha Sree's developer portfolio, contact form, analytics, and AI resume assistant.",
    version="1.0.0"
)

# Enable CORS for local testing and deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- PYDANTIC SCHEMAS -----------------
class ContactRequest(BaseModel):
    name: str
    email: str
    message: str

class ContactResponse(BaseModel):
    success: bool
    message: str
    message_id: int
    timestamp: str

class MessageItem(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class StatsResponse(BaseModel):
    total_views: int
    total_messages: int


# ----------------- API ENDPOINTS -----------------

@app.get("/api/health", tags=["System"])
def health_check():
    """System health check"""
    return {"status": "online", "developer": "Usha Sree Thota", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/contact", response_model=ContactResponse, tags=["Contact"])
def submit_contact(req: ContactRequest, db: Session = Depends(get_db)):
    """
    Submits a recruiter/visitor contact form message into the SQLite database.
    """
    if not req.name.strip() or not req.message.strip():
        raise HTTPException(status_code=400, detail="Name and message cannot be empty")

    new_msg = ContactMessage(
        name=req.name.strip(),
        email=req.email.strip(),
        message=req.message.strip(),
        created_at=datetime.utcnow()
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    return ContactResponse(
        success=True,
        message=f"Thank you, {new_msg.name}! Your message has been received by Usha.",
        message_id=new_msg.id,
        timestamp=new_msg.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    )


@app.get("/api/contact", response_model=List[MessageItem], tags=["Contact"])
def list_messages(db: Session = Depends(get_db)):
    """
    Retrieves all received contact messages (for Usha / Admin review).
    """
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return [
        MessageItem(
            id=m.id,
            name=m.name,
            email=m.email,
            message=m.message,
            created_at=m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        for m in messages
    ]


@app.delete("/api/contact/{message_id}", tags=["Contact"])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Deletes a contact message by ID"""
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return {"success": True, "message": f"Message {message_id} deleted"}


@app.post("/api/visit", tags=["Analytics"])
def record_visit(request: Request, db: Session = Depends(get_db)):
    """
    Records a page view and increments the live visitor counter.
    """
    stat = db.query(SiteStat).first()
    if not stat:
        stat = SiteStat(total_views=1)
        db.add(stat)
    else:
        stat.total_views += 1

    user_agent = request.headers.get("user-agent", "unknown")
    log = VisitorLog(user_agent=user_agent[:250], visited_at=datetime.utcnow())
    db.add(log)
    db.commit()

    return {"total_views": stat.total_views}


@app.get("/api/stats", response_model=StatsResponse, tags=["Analytics"])
def get_stats(db: Session = Depends(get_db)):
    """
    Returns total page views and total contact messages received.
    """
    stat = db.query(SiteStat).first()
    total_views = stat.total_views if stat else 0
    total_messages = db.query(ContactMessage).count()

    return StatsResponse(total_views=total_views, total_messages=total_messages)


@app.post("/api/chat", response_model=ChatResponse, tags=["AI Resume Assistant"])
def chat_with_usha_ai(req: ChatRequest):
    """
    Answers recruiter queries about Usha Sree's resume, skills, projects, and availability.
    """
    query = req.message.strip()
    if not query:
        return ChatResponse(reply="Please type a question about Usha's education, skills, or projects!")

    reply = get_ai_response(query)
    return ChatResponse(reply=reply)


# ----------------- STATIC FRONTEND SERVING -----------------
# Serve frontend files directly from the parent portfolio folder
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Portfolio frontend index.html not found"}

# Mount parent directory for style.css, script.js, resume.pdf
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
