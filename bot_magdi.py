import telebot
import time
import os
from core.database import SessionLocal
from core.models import Project
from requests.exceptions import ReadTimeout, ConnectionError

# بيانات الوصول
API_TOKEN = '8781989622:AAFYsD_HdMFLo7JaaTI0AfyUXv53bz-OWTw'
ADMIN_ID = 7716685142 

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

def is_admin(user_id):
    return user_id == ADMIN_ID

# --- الأوامر الأساسية ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ نأسف، هذا البوت خاص بالمبرمج مجدي فقط.")
        return
    bot.reply_to(message, "أهلاً بك يا مدير مجدي! 👑\n\n/list - عرض المشاريع\n/stats - الإحصائيات\n/add - إضافة مشروع جديد\n/delete - حذف مشروع")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if not is_admin(message.from_user.id): return
    db = SessionLocal()
    count = db.query(Project).count()
    db.close()
    
    report = f"📊 **إحصائيات النظام:**\n\n"
    report += f"📁 عدد المشاريع الكلي: {count}\n"
    report += f"📡 حالة السيرفر: 🟢 يعمل كنشط\n"
    report += f"👤 المسؤول: مجدي العريقي"
    bot.send_message(message.chat.id, report, parse_mode='Markdown')

@bot.message_handler(commands=['list'])
def list_projects(message):
    if not is_admin(message.from_user.id): return
    db = SessionLocal()
    projects = db.query(Project).all()
    db.close()
    if not projects:
        bot.send_message(message.chat.id, "❌ لا توجد مشاريع مضافة.")
    else:
        res = "🗂 **مشاريعك الحالية:**\n"
        for p in projects:
            res += f"🆔 {p.id} | 📌 {p.title}\n"
        bot.send_message(message.chat.id, res, parse_mode='Markdown')

# --- عملية الإضافة ---

@bot.message_handler(commands=['add'])
def ask_title(message):
    if not is_admin(message.from_user.id): return
    msg = bot.send_message(message.chat.id, "📝 أرسل (عنوان المشروع):")
    bot.register_next_step_handler(msg, save_title)

def save_title(message):
    user_data['title'] = message.text
    msg = bot.send_message(message.chat.id, "📖 أرسل (وصف المشروع):")
    bot.register_next_step_handler(msg, save_description)

def save_description(message):
    user_data['description'] = message.text
    msg = bot.send_message(message.chat.id, "🔗 أرسل (رابط المشروع):")
    bot.register_next_step_handler(msg, save_project_db)

def save_project_db(message):
    try:
        db = SessionLocal()
        new_p = Project(title=user_data['title'], description=user_data['description'], link=message.text)
        db.add(new_p)
        db.commit()
        db.close()
        bot.send_message(message.chat.id, "✅ تم الحفظ بنجاح!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ: {e}")

# --- عملية الحذف ---

@bot.message_handler(commands=['delete'])
def ask_id(message):
    if not is_admin(message.from_user.id): return
    msg = bot.send_message(message.chat.id, "🗑 أرسل رقم (ID) المشروع لحذفه:")
    bot.register_next_step_handler(msg, confirm_delete)

def confirm_delete(message):
    if message.text.isdigit():
        db = SessionLocal()
        p = db.query(Project).filter(Project.id == int(message.text)).first()
        if p:
            db.delete(p)
            db.commit()
            bot.send_message(message.chat.id, f"🗑 تم حذف المشروع {message.text} بنجاح.")
        else:
            bot.send_message(message.chat.id, "⚠️ الرقم غير موجود.")
        db.close()

# --- تشغيل البوت مع الحماية من التوقف ---
print("🚀 البوت يعمل الآن بكامل طاقته يا مجدي...")

while True:
    try:
        bot.infinity_polling(timeout=90, long_polling_timeout=50)
    except Exception as e:
        print(f"🔄 إعادة اتصال بسبب: {e}")
        time.sleep(5)
