import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()
# Убедись, что в Render в Environment Variables добавлен BOT_TOKEN
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Добавлены слэши в конце URL
SITES = {
    "GitHub": "https://github.com", 
    "VK": "https://vk.com", 
    "Steam": "https://steamcommunity.com"
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🕵️ Шерлок на связи. Пришли ник.")

# Исправлено: добавлен content_types=
@bot.message_handler(content_types=)
def search(m):
    q = m.text.strip()
    res = [f"🔍 Поиск: `{q}`"]
    
    for n, u in SITES.items():
        try:
            # Проверяем доступность профиля
            response = requests.get(u + q, timeout=5)
            if response.status_code == 200:
                res.append(f"✅ {n}: {u}{q}")
        except Exception:
            continue
            
    if len(res) > 1:
        bot.send_message(m.chat.id, "\n".join(res), parse_mode="Markdown")
    else:
        bot.send_message(m.chat.id, "❌ Ничего не найдено")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
    
