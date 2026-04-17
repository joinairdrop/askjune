import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
JUNE_API_KEY = os.getenv('JUNE_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = OpenAI(
    api_key=JUNE_API_KEY,
    base_url="https://api.blockchain.info/ai/api/v1"   # ← Base URL yang BENAR
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """✅ **AskJune Bot sudah terhubung!**

Sekarang menggunakan model resmi AskJune (`blockchain/june`).

Ketik apa saja untuk test.

Contoh:
- Halo
- Siapa presiden Indonesia sekarang?
- Jelaskan Bitcoin secara singkat""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = client.chat.completions.create(
            model="blockchain/june",      # ← Model resmi AskJune
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{str(e)[:400]}")

print("✅ AskJune Bot V9.2 (menggunakan model blockchain/june) sudah nyala!")
bot.infinity_polling()