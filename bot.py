import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
JUNE_API_KEY = os.getenv('JUNE_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Base URL yang BENAR untuk AskJune / Blockchain.com AI
client = OpenAI(
    api_key=JUNE_API_KEY,
    base_url="https://api.blockchain.info/ai/api/v1"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """✅ **AskJune Bot sudah terhubung dengan Blockchain.com AI!**

Kamu punya 1,000 credits.

Ketik apa saja untuk test.

Contoh:
- Halo
- Siapa presiden Indonesia sekarang?
- Jelaskan cara kerja Bitcoin""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",           # atau coba "claude-3.5-sonnet"
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{str(e)[:400]}")

print("✅ Bot AskJune (Blockchain.com) sudah nyala!")
bot.infinity_polling()