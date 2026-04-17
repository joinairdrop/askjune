import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
JUNE_API_KEY = os.getenv('JUNE_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Setup AskJune AI
client = OpenAI(
    api_key=JUNE_API_KEY,
    base_url="https://api.askjune.ai/v1"
)

user_histories = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """👋 **Bot AskJune AI Siap!**

Sekarang kamu terhubung dengan AskJune AI.

Ketik apa saja, aku akan jawab pakai AskJune.

Contoh:
- "Siapa presiden Indonesia sekarang?"
- "Buat cerita pendek tentang robot"
- "Apa itu Bitcoin?"

Gas chat! 🔥""")

@bot.message_handler(commands=['clear'])
def clear_history(message):
    user_histories[message.chat.id] = []
    bot.reply_to(message, "✅ Memory chat sudah dihapus!")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')

    if chat_id not in user_histories:
        user_histories[chat_id] = []

    try:
        text = message.text.strip()

        user_histories[chat_id].append({"role": "user", "content": text})
        if len(user_histories[chat_id]) > 20:
            user_histories[chat_id] = user_histories[chat_id][-20:]

        response = client.chat.completions.create(
            model="gpt-4o",           # Bisa diganti: claude-3.5-sonnet, grok-beta, dll
            messages=user_histories[chat_id]
        )

        reply = response.choices[0].message.content

        user_histories[chat_id].append({"role": "assistant", "content": reply})
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)[:200]}")

print("✅ Bot AskJune AI sudah nyala!")
bot.infinity_polling()