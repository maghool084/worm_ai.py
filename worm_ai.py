import os
import telebot
import requests
from threading import Thread
from flask import Flask

# --- الإعدادات: سيتم جلب المفاتيح من إعدادات ريندر ---
# إذا كنت قد وضعت المتغيرات في ريندر، سيقرأها الكود تلقائياً
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '8845747802:AAF1UoiTTsFZjP0NINThBa1We6fs4FErMv4')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') # سيأخذ المفتاح من إعدادات Environment
DEVELOPER_USER = "@Maghoo084"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# نظام التنشيط للبقاء 24/7
app = Flask('')
@app.route('/')
def home():
    return "Worm AI is active."

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"أهلاً بك في خدمة Worm AI التقنية.\n\n"
        f"أنا نظام ذكاء اصطناعي متخصص في تقديم حلول برمجية وأدوات تقنية متقدمة.\n"
        f"👤 **المطور:** {DEVELOPER_USER}\n"
        f"أنا هنا للمساعدة، يمكنك طرح أي استفسار تقني وسأقوم بالرد عليك."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not OPENROUTER_API_KEY:
        bot.reply_to(message, "⚠️ خطأ في الإعدادات: لم يتم العثور على مفتاح API في المتغيرات.")
        return

    user_prompt = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": "أنت خبير تقني محترف، ردودك مباشرة ومختصرة. وفر الحلول التقنية والأكواد البرمجية باللغة العربية."},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload).json()
        if 'choices' in response:
            bot.reply_to(message, response['choices'][0]['message']['content'])
        else:
            bot.reply_to(message, "⚠️ فشل الاتصال بخدمة الذكاء الاصطناعي.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ خطأ تقني: {str(e)}")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling(none_stop=True)
