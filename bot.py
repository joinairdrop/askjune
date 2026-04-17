import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
JUNE_API_KEY = os.getenv('JUNE_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Setup AskJune dengan konfigurasi yang lebih aman
client = OpenAI(
    api_key=JUNE_API_KEY,
    base_url="https://api.askjune.ai/v1"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """👋 **AskJune Bot sudah terhubung!**

Sekarang bot ini menggunakan AskJune AI.

Ketik apa saja untuk test.

Contoh:
- Halo
- Siapa presiden Indonesia?
- Apa itu Bitcoin?

Gas! 🔥""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",                    # Model default yang paling stabil
            messages=[{"role": "user", "content": message.text}],
            timeout=60
        )
        bot.reply_to(message, response.choices[0].message.content)
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "authentication" in error_msg.lower():
            bot.reply_to(message, "❌ API Key AskJune tidak valid atau belum aktif.")
        elif "404" in error_msg or "not found" in error_msg.lower():
            bot.reply_to(message, "❌ Base URL AskJune salah.")
        else:
            bot.reply_to(message, f"❌ Connection Error:\n{error_msg[:300]}")

print("✅ AskJune Bot V9.1 sedang berjalan...")
bot.infinity_polling()