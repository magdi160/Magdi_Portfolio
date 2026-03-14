import telebot
from telebot import types
import sys
import os
from dotenv import load_dotenv

# تحميل التوكن من الملف السري
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_TOKEN')

# إعداد المسارات
path = '/home/magdi160/Magdi_Portfolio'
if path not in sys.path:
    sys.path.append(path)

from core.database import SessionLocal
from core.models import Project

bot = telebot.TeleBot(API_TOKEN)

# --- القفل الأمني (ID مجدي) ---
MY_ID = 7716685142

def is_it_me(message):
    if message.chat.id == MY_ID:
        return True
    else:
        bot.reply_to(message, "⚠️ عذراً، هذا البوت خاص بالمبرمج مجدي فقط.")
        return False

# لوحة التحكم
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚀 إضافة مشروع')
    btn2 = types.KeyboardButton('📂 عرض المشاريع')
    btn3 = types.KeyboardButton('✏️ تعديل مشروع')
    btn4 = types.KeyboardButton('❌ حذف مشروع')
    btn5 = types.KeyboardButton('📊 حالة السيرفر')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_it_me(message):
        bot.reply_to(message, "أهلاً بك يا مجدي في لوحة التحكم الآمنة! 🔐", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not is_it_me(message):
        return

    if message.text == '🚀 إضافة مشروع':
        msg = bot.reply_to(message, "أرسل اسم المشروع الجديد:")
        bot.register_next_step_handler(msg, process_title)
    
    elif message.text == '📂 عرض المشاريع':
        db = SessionLocal()
        projects = db.query(Project).all()
        db.close()
        res = "📋 قائمة مشاريعك:\n" + "\n".join([f"🆔 {p.id} | {p.title}" for p in projects])
        bot.send_message(message.chat.id, res)

    elif message.text == '📊 حالة السيرفر':
        bot.reply_to(message, "السيرفر يعمل بكفاءة يا مجدي ✅")

def process_title(message):
    title = message.text
    db = SessionLocal()
    new_project = Project(title=title, description="مشروع مضاف عبر البوت الآمن", tech_stack="Python", link="#", image_url="https://via.placeholder.com/300")
    db.add(new_project)
    db.commit()
    db.close()
    bot.reply_to(message, f"✅ تم إضافة '{title}'!", reply_markup=main_keyboard())

print("البوت مؤمن ويعمل الآن لمجدي فقط...")
bot.polling(none_stop=True)
