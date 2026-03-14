from core.database import SessionLocal
from core.models import Project

def list_projects():
    db = SessionLocal()
    projects = db.query(Project).all()
    print("\n--- قائمة المشاريع الحالية ---")
    for p in projects:
        print(f"[{p.id}] - {p.title}")
    db.close()
    return projects

def delete_project(project_id):
    db = SessionLocal()
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        print(f"✅ تم حذف المشروع بنجاح.")
    else:
        print("❌ لم يتم العثور على المشروع.")
    db.close()

def update_project(project_id):
    db = SessionLocal()
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        print(f"تعديل المشروع: {project.title}")
        project.title = input(f"الاسم الجديد ({project.title}): ") or project.title
        project.description = input(f"الوصف الجديد: ") or project.description
        db.commit()
        print("✅ تم التحديث بنجاح.")
    db.close()

if __name__ == "__main__":
    list_projects()
    choice = input("\nماذا تريد أن تفعل؟ (1: حذف، 2: تعديل، 3: خروج): ")
    if choice == '1':
        p_id = input("أدخل رقم (ID) المشروع للحذف: ")
        delete_project(int(p_id))
    elif choice == '2':
        p_id = input("أدخل رقم (ID) المشروع للتعديل: ")
        update_project(int(p_id))
