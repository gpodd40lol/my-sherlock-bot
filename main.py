import os
import telebot
from dotenv import load_dotenv
import osint_tools as osint # Импортируем наши инструменты

load_dotenv()
token = "8739255331:AAHoQkAzn1Gmese9hn0_AgFpjXPuCIQdXCs"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(m):
    text = (
        "🕵️ **OSINT Бот готов к работе.**\n\n"
        "Отправь мне:\n"
        "• **Никнейм** — для поиска по соцсетям\n"
        "• **IP адрес** — для геолокации сервера\n"
        "• **Email** — для проверки утечек"
    )
    bot.send_message(m.chat.id, text, parse_mode="Markdown")

@bot.message_handler(content_types=)
def handle_search(m):
    q = m.text.strip()
    chat_id = m.chat.id
    
    bot.send_message(chat_id, f"🔍 Начинаю сбор данных по запросу: `{q}`...", parse_mode="Markdown")

    results = []

    # 1. Если это IP
    if q.count('.') == 3 and q.replace('.', '').isdigit():
        results += ["--- [ IP ИНФОРМАЦИЯ ] ---"]
        results += osint.search_ip(q)
    
    # 2. Если это почта
    elif "@" in q:
        results += ["--- [ ПРОВЕРКА ПОЧТЫ ] ---"]
        results += osint.check_mail_leak(q)
    
    # 3. Иначе считаем это никнеймом
    else:
        results += ["--- [ СОЦИАЛЬНЫЕ СЕТИ ] ---"]
        res_socials = osint.search_socials(q)
        if res_socials:
            results += res_socials
        else:
            results.append("❌ Профилей не найдено")

    final_text = "\n".join(results)
    bot.send_message(chat_id, final_text if results else "Ничего не найдено.")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
    
