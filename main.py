import os
import telebot
import requests
import threading
import http.server
import socketserver

# 1. Заглушка для Render
def run_health_check():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()

# 2. Настройка бота (ВСТАВЬ СВОЙ ТОКЕН НИЖЕ)
TOKEN = "8739255331:AAHoQkAzC_v8m0k4q6r7e_m6"
bot = telebot.TeleBot(TOKEN)

# 3. База поиска
SITES = {
    "GitHub": "https://github.com",
    "VK": "https://vk.com",
    "Steam": "https://steamcommunity.com",
    "Telegram": "https://t.me"
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🕵️ Бот запущен. Пришли ник.")

@bot.message_handler(func=lambda message: True)
def search(m):
    q = m.text.strip()
    res = [f"🔍 Поиск: `{q}`"]
    for name, base_url in SITES.items():
        try:
            url = base_url + q
            if requests.get(url, timeout=5).status_code == 200:
                res.append(f"✅ {name}: {url}")
        except: continue
    bot.send_message(m.chat.id, "\n".join(res) if len(res) > 1 else "❌ Не нашел", parse_mode="Markdown")

if __name__ == '__main__':
    bot.infinity_polling()
    
