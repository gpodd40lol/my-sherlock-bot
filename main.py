import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

SITES = {"GitHub": "https://github.com", "VK": "https://vk.com", "Steam": "https://steamcommunity.com"}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🕵️ Шерлок на связи. Пришли ник или IP.")

@bot.message_handler(content_types=)
def search(m):
    q = m.text.strip()
    res = [f"🔍 Поиск: `{q}`"]
    for n, u in SITES.items():
        try:
            if requests.get(u + q, timeout=5).status_code == 200: res.append(f"✅ {n}: {u}{q}")
        except: continue
    bot.send_message(m.chat.id, "\n".join(res) if len(res) > 1 else "❌ Не нашел", parse_mode="Markdown")

if __name__ == '__main__':
    bot.infinity_polling()
    
