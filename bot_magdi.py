import telebot
from telebot import types
import sys
import os

# إعداد المسارات لربط قاعدة البيانات
path = '/home/magdi160/Magdi_Portfolio'
if path not in sys.path:
    sys.path.append(path)

from core.database import SessionLocal
from core.models import Project

# التوكن والآيدي الخاص بك
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
MY_ID = YOUR_CHAT_ID_HERE

bot = telebot.TeleBot(API_TOKEN)

# دالة التحقق من الهوية
def is_it_me(message):
    if message.chat.id == MY_ID:
        return True
    bot.reply_to(message, "⚠️ عذراً مجدي، هذا البوت مؤمن.")
    return False

# لوحة التحكم الكاملة
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚀 إضافة مشروع')
    btn2 = types.KeyboardButton('📂 عرض المشاريع')
    btn3 = types.KeyboardButton('✏️ تعديل عنوان')
    btn4 = types.KeyboardButton('❌ حذف مشروع')
    btn5 = types.KeyboardButton('📊 حالة السيرفر')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_it_me(message):
        bot.reply_to(message, "مرحباً يا مجدي! لوحة التحكم الكاملة جاهزة للعمل 🛠", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not is_it_me(message): return

    if message.text == '🚀 إضافة مشروع':
        msg = bot.reply_to(message, "أرسل اسم المشروع الجديد:")
        bot.register_next_step_handler(msg, process_add)
    
    elif message.text == '📂 عرض المشاريع':
        db = SessionLocal()
        projects = db.query(Project).all()
        db.close()
        res = "📋 **مشاريعك الحالية:**\n"
        res += "\n".join([f"🆔 **{p.id}** | {p.title}" for p in projects])
        bot.send_message(message.chat.id, res if projects else "لا توجد مشاريع.")

    elif message.text == '❌ حذف مشروع':
        msg = bot.reply_to(message, "أرسل رقم (ID) المشروع لحذفه:")
        bot.register_next_step_handler(msg, process_delete)

    elif message.text == '✏️ تعديل عنوان':
        msg = bot.reply_to(message, "أرسل رقم (ID) المشروع لتعديله:")
        bot.register_next_step_handler(msg, process_edit_id)

    elif message.text == '📊 حالة السيرفر':
        bot.reply_to(message, "السيرفر يعمل في الخلفية بنظام nohup ✅")

# --- دوال المعالجة ---
def process_add(message):
    title = message.text
    db = SessionLocal()
    new_project = Project(title=title, description="مشروع جديد", tech_stack="Python", link="#", image_url="https://via.placeholder.com/300")
    db.add(new_project)
    db.commit()
    db.close()
    bot.reply_to(message, f"✅ تم إضافة '{title}' بنجاح!", reply_markup=main_keyboard())

def process_delete(message):
    db = SessionLocal()
    project = db.query(Project).filter(Project.id == message.text).first()
    if project:
        db.delete(project)
        db.commit()
        bot.reply_to(message, "✅ تم الحذف بنجاح.")
    else:
        bot.reply_to(message, "❌ الرقم غير موجود.")
    db.close()

def process_edit_id(message):
    project_id = message.text
    msg = bot.reply_to(message, "أرسل العنوان الجديد:")
    bot.register_next_step_handler(msg, process_edit_final, project_id)

def process_edit_final(message, project_id):
    db = SessionLocal()
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.title = message.text
        db.commit()
        bot.reply_to(message, "✅ تم التعديل.")
    db.close()

print("البوت الكامل شغال...")
bot.polling(none_stop=True)
