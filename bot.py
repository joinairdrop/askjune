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
    bot.reply_to(message, f"""AskJune Bot Diagnostic

Token Telegram: ✅ OK
API Key AskJune: {'✅ Ada' if JUNE_API_KEY else '❌ Kosong'}

Ketik apa saja untuk test koneksi ke AskJune.""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}],
            timeout=30
        )
        bot.reply_to(message, response.choices[0].message.content)
        
    except Exception as e:
        error = str(e)
        bot.reply_to(message, f"""❌ Connection Error

Error message:
{error[:500]}

Solusi yang bisa dicoba:
1. Cek apakah API Key AskJune sudah aktif
2. Cek quota / limit di dashboard AskJune
3. Coba ganti model ke "claude-3.5-sonnet" atau "grok-beta" kalau tersedia""")

print("Bot running with diagnostic mode...")
bot.infinity_polling()