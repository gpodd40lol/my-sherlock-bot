import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

SITES = {
    "GitHub": "https://github.com",
    "VK": "https://vk.com",
    "Steam": "https://steamcommunity.com",
    "OK": "https://ok.ru"
}

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    await m.answer("🕵️ Пришли ник или IP.")

@dp.message_handler()
async def search(m: types.Message):
    query = m.text.strip()
    res = []
    
    async with aiohttp.ClientSession() as session:
        # Чекаем ник
        for name, url in SITES.items():
            try:
                async with session.get(url + query, timeout=5) as r:
                    if r.status == 200:
                        res.append(f"✅ {name}: {url}{query}")
            except: continue
        
        # Чекаем IP
        ip_url = f"http://ip-api.com{query}?fields=status,country,city,isp"
        try:
            async with session.get(ip_url) as r:
                data = await r.json()
                if data.get('status') == 'success':
                    res.append(f"\n🌐 IP: {data['country']}, {data['city']}\n🏢 ISP: {data['isp']}")
        except: pass

    await m.answer("\n".join(res) if res else "❌ Пусто.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
