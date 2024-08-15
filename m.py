import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace with your bot token
BOT_TOKEN = 'your_bot_token_here'
CHAT_ID = 'your_chat_id_here'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send me a list of BINs (one per line) to check if they are VBV or not.")

def check_bin(bin_number):
    result = f"BIN {bin_number}: "
    if str(bin_number).startswith('4'):
        try:
            response = requests.get(f"https://lookup.binlist.net/{bin_number}")
            if response.status_code == 200:
                data = response.json()
                if data.get("scheme") == "visa" and data.get("prepaid") is False:
                    result += "VBV (Verified by Visa)"
                else:
                    result += "Not VBV"
            else:
                result += "Failed to retrieve information"
        except Exception as e:
            result += f"Error: {e}"
    else:
        result += "Not a Visa BIN"
    return result

def handle_bins(update: Update, context: CallbackContext) -> None:
    bins = update.message.text.splitlines()
    bot = context.bot
    results = []
    
    for bin_number in bins:
        result = check_bin(bin_number.strip())
        results.append(result)
    
    message = "\n".join(results)
    bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_bins))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
