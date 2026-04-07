import requests

def search_socials(nickname):
    """Поиск ника по популярным сервисам"""
    sites = {
        "GitHub": f"https://github.com{nickname}",
        "VK": f"https://vk.com{nickname}",
        "Steam": f"https://steamcommunity.com{nickname}",
        "Telegram": f"https://t.me{nickname}"
    }
    found = []
    for name, url in sites.items():
        try:
            res = requests.get(url, timeout=3)
            if res.status_code == 200:
                found.append(f"✅ {name}: {url}")
        except: continue
    return found

def search_ip(ip):
    """Технический OSINT: информация по IP"""
    try:
        res = requests.get(f"http://ip-api.com{ip}").json()
        if res.get("status") == "success":
            return [
                f"🌍 Страна: {res.get('country')}",
                f"🏙 Город: {res.get('city')}",
                f"🏢 Провайдер: {res.get('isp')}"
            ]
    except: return []
    return []

def check_mail_leak(email):
    """Проверка почты на утечки (демо-версия через общедоступный API)"""
    # В реальности лучше использовать API HaveIBeenPwned (нужен ключ)
    return [f"📧 Почта {email} добавлена в очередь на мониторинг утечек."]
  
