from flask import Flask, render_template
import os
import sys

# ضمان أن السيرفر يرى مجلد المشروع والمجلدات الفرعية
path = '/home/magdi160/Magdi_Portfolio'
if path not in sys.path:
    sys.path.append(path)

from core.database import SessionLocal
from core.models import Project

app = Flask(__name__, template_folder="templates")

@app.route("/")
def read_root():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        return render_template("index.html", projects=projects)
    except Exception as e:
        return f"خطأ في قاعدة البيانات أو القالب: {str(e)}"
    finally:
        db.close()

if __name__ == "__main__":
    app.run()
