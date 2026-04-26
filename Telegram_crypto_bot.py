import telebot
import requests
import time
import threading
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID")

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

def get_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        data = requests.get(url, timeout=10).json()
        return float(data["price"])
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "<b>bot online 24/7</b>\n\ncommands: /price /all")

@bot.message_handler(commands=['price'])
def price(message):
    btc = get_price()
    if btc:
        bot.reply_to(message, f"<b>Bitcoin:</b> ${btc:,.0f}")
    else:
        bot.reply_to(message, "price fetch failed")

@bot.message_handler(commands=['all'])
def all_prices(message):
    btc = get_price("BTCUSDT")
    eth = get_price("ETHUSDT")
    if btc and eth:
        bot.reply_to(message, f"""<b>crypto prices:</b>

    btc: ${btc:,.0f}
    eth: ${eth:,.0f}""")
    else:
        bot.reply_to(message, "price fetch failed")

def hourly_alert():
    while True:
        btc = get_price()
        if btc:
            try:
                bot.send_message(CHAT_ID, f"hourly btc: <b>${btc:,.0f}</b>")
            except:
                pass
        time.sleep(3600)

if __name__ == "main":
    print("bot started - running 24/7 version")
    threading.Thread(target=hourly_alert, daemon=True).start()
    bot.infinity_polling()
