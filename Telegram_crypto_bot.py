import os
import telebot
import requests
import time
import threading
from flask import Flask
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN") or "8638479869:AAFERYiFmeFx88nSPltakB0ePcbGcVGQIKU"
CHAT_ID = int(os.getenv("CHAT_ID") or 5345408320)
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
app = Flask(__name__)
def get_price(coin="BTC"):
    try:
        if coin == "BTC":
            url = "https://blockchain.info"
            response = requests.get(url, timeout=10)
            return float(response.json()['USD']['last'])
        elif coin == "ETH":
            url = "https://cryptocompare.com"
            response = requests.get(url, timeout=10)
            return float(response.json()['USD'])
        return None
    except:
        return None
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "bot online 24/7\n\ncommands: /price /all")
@bot.message_handler(commands=['price'])
def price(message):
    btc = get_price("BTC")
    if btc:
        bot.reply_to(message, f"bitcoin: ${btc:,.0f}")
    else:
        bot.reply_to(message, "price fetch failed")
@bot.message_handler(commands=['all'])
def all_prices(message):
    btc = get_price("BTC")
    eth = get_price("ETH")
    if btc and eth:
        bot.reply_to(message, f"crypto prices\n\nbtc: ${btc:,.0f}\neth: ${eth:,.0f}")
    else:
        bot.reply_to(message, "price fetch failed")
def hourly_alert():
    while True:
        btc = get_price("BTC")
        if btc:
            try:
                bot.send_message(CHAT_ID, f"hourly report btc: ${btc:,.0f}")
            except:
                pass
        time.sleep(3600)
@app.route('/')
def index():
    return "alive"
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
if __name__ == "__main__":
    print("bot started")
    threading.Thread(target=hourly_alert, daemon=True).start()
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
