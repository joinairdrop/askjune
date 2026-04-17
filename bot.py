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
    base_url="https://api.blockchain.info/ai/api/v1"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """✅ **AskJune Bot Test**

API Key terdeteksi.

Coba ketik pertanyaan apa saja.

Saya akan mencoba beberapa model yang mungkin didukung.""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    models_to_try = ["claude-3.5-sonnet", "gpt-4o-mini", "grok-beta", "claude-3-opus"]

    for model in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message.text}]
            )
            bot.reply_to(message, f"**Model: {model}**\n\n{response.choices[0].message.content}")
            return   # Kalau berhasil, stop di model pertama yang jalan

        except Exception as e:
            continue  # Coba model berikutnya kalau gagal

    # Kalau semua model gagal
    bot.reply_to(message, "❌ Semua model yang dicoba gagal.\nMungkin API Key belum memiliki akses model chat.")

print("✅ Bot AskJune dengan multiple model test sudah nyala!")
bot.infinity_polling()