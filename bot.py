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
    base_url="https://api.askjune.ai/v1"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Bot AskJune AI sedang diuji.\nKetik apa saja untuk test.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",        # coba ganti ke "claude-3.5-sonnet" kalau ada
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
        
    except Exception as e:
        error_text = str(e)
        bot.reply_to(message, f"❌ Connection Error:\n{error_text[:400]}")

print("Bot running...")
bot.infinity_polling()