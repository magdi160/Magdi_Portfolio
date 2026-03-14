from core.database import SessionLocal
from core.models import Project

def add_new_project(title, description, tech, link, image):
    db = SessionLocal()
    new_project = Project(
        title=title,
        description=description,
        tech_stack=tech,
        link=link,
        image_url=image
    )
    db.add(new_project)
    db.commit()
    db.close()
    print(f"✅ تم إضافة مشروع '{title}' بنجاح!")

if __name__ == "__main__":
    # هنا تضع بيانات مشروعك الجديد
    print("--- إضافة مشروع جديد ---")
    t = input("اسم المشروع: ")
    d = input("وصف المشروع: ")
    ts = input("التقنيات المستخدمة (مثلاً Python, SQL): ")
    l = input("رابط المشروع (أو هاتف التواصل): ")
    img = "default.jpg" # يمكنك تغييرها لاحقاً
    
    add_new_project(t, d, ts, l, img)
