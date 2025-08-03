import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, run_async

BOT_TOKEN = os.getenv("BOT_TOKEN")
IVASMS_CODE = os.getenv("IVASMS_CODE")
AVAILABLE = []

USER_MAP = {}

def get_sms(code, number):
    url = f"https://www.ivasms.com/portal/smsbox/{code}/{number}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    found = soup.find("div", class_="otp-code")
    return found.text.strip() if found else "কোড পাওয়া যায়নি"

def start(update: Update, ctx: CallbackContext):
    update.message.reply_text("Welcome! Use /get_number or /get_code")

def get_number(update: Update, ctx: CallbackContext):
    uid = update.effective_user.id
    if uid not in USER_MAP:
        if AVAILABLE:
            num = AVAILABLE.pop(0)
            USER_MAP[uid] = num
            update.message.reply_text(f"Your number: {num}")
        else:
            update.message.reply_text("No numbers left.")
    else:
        update.message.reply_text(f"You already have: {USER_MAP[uid]}")

def get_code(update: Update, ctx: CallbackContext):
    uid = update.effective_user.id
    if uid in USER_MAP:
        code_text = get_sms(IVASMS_CODE, USER_MAP[uid])
        update.message.reply_text(f"Code for {USER_MAP[uid]}:\n{code_text}")
    else:
        update.message.reply_text("প্রথমে /get_number করো")

def main():
    global AVAILABLE
    AVAILABLE = ["019xxxxxxxx", "018yyyyyyyy"]  # এখানে নাম্বারগুলো বসাও
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_number", get_number))
    dp.add_handler(CommandHandler("get_code", get_code))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
