import os
import telebot
import requests
import threading
import http.server
import socketserver
from dotenv import load_dotenv

# 1. КОСТЫЛЬ ДЛЯ RENDER (чтобы не засыпал)
def run_health_check():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()

# 2. НАСТРОЙКА БОТА
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") or "8739255331:AAHoQkAzn1Gmese9hn0_AgFpjXPuCIQdXCs"
bot = telebot.TeleBot(TOKEN)

# 3. ЛОГИКА ПОИСКА
SITES = {
    "GitHub": "https://github.com",
    "VK": "https://vk.com",
    "Steam": "https://steamcommunity.com",
    "Telegram": "https://t.me"
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🕵️ OSINT Бот запущен. Пришли никнейм для поиска.")

@bot.message_handler(content_types=)
def search(m):
    nick = m.text.strip()
    res = [f"🔍 Результаты для: `{nick}`"]
    
    # Поиск по соцсетям
    for name, url in SITES.items():
        try:
            full_url = url + nick
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                res.append(f"✅ {name}: {full_url}")
        except:
            continue
            
    # Поиск по IP (если ввели IP)
    if nick.count('.') == 3 and nick.replace('.', '').isdigit():
        try:
            ip_info = requests.get(f"http://ip-api.com{nick}").json()
            if ip_info['status'] == 'success':
                res.append(f"\n🌍 IP: {ip_info['country']}, {ip_info['city']}\n🏢 ISP: {ip_info['isp']}")
        except: pass

    bot.send_message(m.chat.id, "\n".join(res) if len(res) > 1 else "❌ Ничего не найдено", parse_mode="Markdown")

if __name__ == '__main__':
    print("🚀 Бот запущен и готов к работе!")
    bot.infinity_polling()
    
