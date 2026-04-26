import telebot
import requests
import time
import threading

# ВСТАВЬ СЮДА СВОИ ДАННЫЕ В КАВЫЧКИ НАПРЯМУЮ
TOKEN = "8638479869:AAFERYiFmeFx88nSPltakB0ePcbGcVGQIKU"
CHAT_ID = 5345408320

bot = telebot.TeleBot(TOKEN)

def get_price():
    # Мы просто возвращаем случайное число, не заходя в интернет
    return 65432.0 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "bot online. use /price")

@bot.message_handler(commands=['price'])
def price(message):
    val = get_price()
    if val:
        bot.reply_to(message, f"btc: ${val:,.0f}")
    else:
        bot.reply_to(message, "fetch failed")

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

