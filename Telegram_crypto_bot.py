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
def get_price(symbol="BTCUSDT"):
    try:
        url = f"https://bybit.com{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        price = float(data['result']['list'][0]['lastPrice'])
        return price
    except Exception as e:
        print(f"Impossible to get the price{symbol}: {e}")
        return None
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "<b>The bot is working 24/7!</b>\n\nКоманды: /price, /all")
@bot.message_handler(commands=['price'])
def price(message):
    btc = get_price("BTCUSDT")
    if btc:
        bot.reply_to(message, f"<b>Bitcoin:</b> ${btc:,.0f}")
    else:
        bot.reply_to(message, "The bot wasnt able to get the price.")
@bot.message_handler(commands=['all'])
def all_prices(message):
    btc = get_price("BTCUSDT")
    eth = get_price("ETHUSDT")
    if btc and eth:
        bot.reply_to(message, f"<b>Курсы валют:</b>\n\nBTC: ${btc:,.0f}\nETH: ${eth:,.0f}")
    else:
        bot.reply_to(message, "Error in finding the price.")
def hourly_alert():
    while True:
        btc = get_price("BTCUSDT")
        if btc:
            try:
                bot.send_message(CHAT_ID, f"Hourly BTC price: <b>${btc:,.0f}</b>")
            except Exception as e:
                print(f"Error of the alert: {e}")
        time.sleep(3600)
@app.route('/')
def index():
    return "Bot is alive"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("Бот запускается...")
    threading.Thread(target=hourly_alert, daemon=True).start()
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
