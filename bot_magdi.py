import telebot
from telebot import types
import sys
import os

path = '/home/magdi160/Magdi_Portfolio'
if path not in sys.path:
    sys.path.append(path)

from core.database import SessionLocal
from core.models import Project

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
MY_ID = YOUR_CHAT_ID_HERE

bot = telebot.TeleBot(API_TOKEN)

def is_it_me(message):
    return message.chat.id == MY_ID

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
        bot.reply_to(message, "لوحة التحكم كاملة الآن يا مجدي! 🛠", reply_markup=main_keyboard())

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
        res = "📋 **مشاريعك:**\n" + "\n".join([f"🆔 {p.id} | {p.title}" for p in projects])
        bot.send_message(message.chat.id, res if projects else "لا توجد مشاريع.")

    elif message.text == '❌ حذف مشروع':
        msg = bot.reply_to(message, "أرسل رقم (ID) المشروع لحذفه:")
        bot.register_next_step_handler(msg, process_delete)

    elif message.text == '✏️ تعديل عنوان':
        msg = bot.reply_to(message, "أرسل رقم (ID) المشروع لتعديله:")
        bot.register_next_step_handler(msg, process_edit_id)

    elif message.text == '📊 حالة السيرفر':
        bot.reply_to(message, "السيرفر يعمل بكفاءة ✅")

def process_add(message):
    db = SessionLocal()
    new_p = Project(title=message.text, description="مشروع جديد", tech_stack="Python", link="#", image_url="https://via.placeholder.com/300")
    db.add(new_p)
    db.commit()
    db.close()
    bot.reply_to(message, "✅ تم الإضافة!", reply_markup=main_keyboard())

def process_delete(message):
    db = SessionLocal()
    p = db.query(Project).filter(Project.id == message.text).first()
    if p:
        db.delete(p)
        db.commit()
        bot.reply_to(message, "✅ تم الحذف.")
    else:
        bot.reply_to(message, "❌ الرقم غير موجود.")
    db.close()

def process_edit_id(message):
    p_id = message.text
    msg = bot.reply_to(message, "أرسل العنوان الجديد:")
    bot.register_next_step_handler(msg, process_edit_final, p_id)

def process_edit_final(message, p_id):
    db = SessionLocal()
    p = db.query(Project).filter(Project.id == p_id).first()
    if p:
        p.title = message.text
        db.commit()
        bot.reply_to(message, "✅ تم التعديل.")
    db.close()

bot.polling(none_stop=True)
