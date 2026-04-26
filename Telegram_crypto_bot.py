import telebot
import requests
import time
import threading
import re

TOKEN = "8638479869:AAFERYiFmeFx88nSPltakB0ePcbGcVGQIKU"
CHAT_ID = 5345408320

bot = telebot.TeleBot(TOKEN)

def get_price():
    try:
        # Идем не на биржу, а в Google Search. Его сервера не банят.
        url = "https://google.com"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=15)
        
        # Ищем число в тексте страницы (грубый, но эффективный метод)
        # Находит что-то похожее на "65,123.45"
        match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\sUnited States Dollar', r.text)
        if match:
            price_str = match.group(1).replace(',', '')
            return float(price_str)
        
        # Если Google не отдал, пробуем легкий API Blockchain.info еще раз с User-Agent
        r2 = requests.get("https://blockchain.info", headers=headers, timeout=10)
        return float(r2.json()['USD']['last'])
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "bot online. use /price")

@bot.message_handler(commands=['price'])
def price(message):
    val = get_price()
    if val:
        bot.reply_to(message, f"bitcoin: ${val:,.0f}")
    else:
        bot.reply_to(message, "price fetch failed")

def alert():
    while True:
        val = get_price()
        if val:
            try:
                bot.send_message(CHAT_ID, f"hourly: ${val:,.0f}")
            except: pass
        time.sleep(3600)

if __name__ == "__main__":
    print("bot is running")
    threading.Thread(target=alert, daemon=True).start()
    bot.infinity_polling()


