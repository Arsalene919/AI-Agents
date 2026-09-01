from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas
from services import generate_report
from auth import hash_password, verify_password, create_access_token, get_current_user
from openai import OpenAI
import subprocess, json

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Research Asssistant API", version="1.0.0")

#Authentication routes
@app.post("/auth/register", response_model=schemas.UserResponse)
def register_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user_obj = models.User(
        email=body.email,
        hashed_password=hash_password(body.password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@app.post("/auth/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user


#Report routes

# Post /reports/generate
@app.post("/reports/generate", response_model=schemas.ReportResponse)
def create_report(body: schemas.ReportCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    content, nb_sources = generate_report(body.topic)
    report = models.Report(
        topic=body.topic,
        content=content,
        sources=nb_sources,
        words=len(content.split()),
        owner_id=current_user.id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@app.post("/agent/ask")
async def agent_ask(body: dict, db: Session = Depends(get_db)):
    """L'agent utilise les outils MCP pour répondre"""
    question = body.get("question")

    # Démarre le serveur MCP
    tools = [
        {"type": "function", "function": {
            "name": "save_report",
            "description": "Sauvegarde un rapport",
            "parameters": {"type": "object",
                "properties": {"topic": {"type": "string"},
                               "content": {"type": "string"}},
                "required": ["topic", "content"]}
        }},
        {"type": "function", "function": {
            "name": "search_reports",
            "description": "Cherche dans les rapports",
            "parameters": {"type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]}
        }}
    ]

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un assistant qui gère des rapports de recherche."},
            {"role": "user", "content": question}
        ],
        tools=tools
    )
    return {"response": response.choices[0].message.content}

#route 1 : liste
@app.get("/reports", response_model=list[schemas.ReportResponse])
def list_reports(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Report).filter(models.Report.owner_id == current_user.id).order_by(models.Report.created_at.desc()).all()

#Route search AVANT la route {report_id}
@app.get("/reports/search/query", response_model=list[schemas.ReportResponse])
def search_reports(q: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Report).filter(
        models.Report.owner_id == current_user.id,
        models.Report.topic.ilike(f"%{q}%")
    ).all()


# Get /reports/{id} route 2
@app.get("/reports/{report_id}", response_model=schemas.ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.owner_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# Delete /reports/{id}
@app.delete("/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.owner_id == current_user.id).first()
    if not report: 
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}

# Get /reports/search?q=topic
@app.get("/reports/search/query", response_model=list[schemas.ReportResponse])
def search_reports(q: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Report).filter(
        models.Report.topic.ilike(f"%{q}%"),
        models.Report.owner_id == current_user.id
    ).all()