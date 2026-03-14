from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from core.database import SessionLocal
from core.models import Project

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    # فتح اتصال بقاعدة البيانات لقراءة المشاريع
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
    finally:
        db.close()
    
    # إرسال المشاريع إلى ملف الـ HTML
    return templates.TemplateResponse("index.html", {"request": request, "projects": projects})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
