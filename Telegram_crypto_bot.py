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
        url = f"https://binance.com{symbol}"
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
def hourly_alert():
    while True:
        btc = get_price()
        if btc:
            try:
                bot.send_message(CHAT_ID, f"hourly btc: <b>${btc:,.0f}</b>")
            except Exception as e:
                print(f"Error sending message: {e}")
        time.sleep(3600)
@app.route('/')
def index():
    return "Bot is running"
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
if __name__ == "__main__":
    print("Starting bot...")
    threading.Thread(target=hourly_alert, daemon=True).start()
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
