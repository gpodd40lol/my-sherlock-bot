import os
import telebot
import requests
from dotenv import load_dotenv

# Загружаем токен
load_dotenv()
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

# Список сайтов для поиска
SITES = {
    "GitHub": "https://github.com",
    "VK": "https://vk.com",
    "Steam": "https://steamcommunity.com",
    "OK": "https://ok.ru"
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🕵️‍♂️ **Шерлок готов.**\nПришли ник или IP для поиска.")

@bot.message_handler(content_types=)
def search(m):
    query = m.text.strip()
    res = [f"🔍 **Результаты для:** `{query}`\n"]
    
    # 1. Поиск по нику
    for name, url in SITES.items():
        try:
            r = requests.get(url + query, timeout=5)
            if r.status_code == 200:
                res.append(f"✅ {name}: {url}{query}")
        except: continue
    
    # 2. Поиск по IP
    try:
        r = requests.get(f"http://ip-api.com{query}", timeout=5)
        data = r.json()
        if data.get('status') == 'success':
            res.append(f"\n🌐 **IP Инфо:**\n📍 {data['country']}, {data['city']}\n🏢 Провайдер: {data['isp']}")
    except: pass

    # Отправка итога
    final_text = "\n".join(res)
    if len(res) <= 1:
        bot.send_message(m.chat.id, "❌ Ничего не нашел.")
    else:
        bot.send_message(m.chat.id, final_text, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()
    
