'''This script runs the Telegram bot for web app.'''

# import libraries
import logging
from credentials import BOT_TOKEN, BOT_USERNAME
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, ContextTypes, InlineQueryHandler, filters
import uuid

web_link = "https://lawun330.github.io/sannie-bot/"

# initiate logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)
logger = logging.getLogger(__name__)


# function for '/start' -> return the inline keyboard
async def start_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
	inline_button = [
        [InlineKeyboardButton("Get BBC Burmese News", web_app=WebAppInfo(web_link))]
    ]
	reply_markup = InlineKeyboardMarkup(inline_button)
	await update.message.reply_text(f"Let's get started 👩🏻‍💼\n\nTo get your latest news 📰, please tap the button below or\ngo to {web_link}", reply_markup=reply_markup)


# function for '/help' -> return the help message
async def help_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text('This bot will present you BBC Burmese news. Try /start')


# function for '/keyboard' -> return the keyboard
async def keyboard_button_function(update: Update, callback: CallbackContext):
    keyboard_button = [
        [KeyboardButton("Get BBC Burmese News", web_app=WebAppInfo(web_link))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard_button, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Check out the keyboard below 👇🏻", reply_markup=reply_markup)


# function for inline method
async def inline_method_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
	logger.info(f"Inline query received: {update.inline_query.query}")
	results = []
	# default result for any query
	default_result = InlineQueryResultArticle(
        id=uuid.uuid4(),
        title="BBC Burmese News",
        description="Get the latest news from BBC Burmese",
        input_message_content=InputTextMessageContent(message_text=web_link)
    )
	results.append(default_result)
	await update.inline_query.answer(results)


# function to echo user's messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'I do not understand your message, you said "{update.message.text}".\n\nIf you need help, try /help'
    )


# main function
if __name__ == "__main__":
	# initiate the bot # pass tokens
	app = ApplicationBuilder().token(BOT_TOKEN).build()
	logger.info("The telegram bot is initiated.") # debugging print

	# create and add handlers to the app
	start_handler = CommandHandler('start', start_function)
	help_handler = CommandHandler('help', help_function)
	keyboard_button_handler = CommandHandler('keyboard', keyboard_button_function)
	inline_method_handler = InlineQueryHandler(inline_method_function)
	echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

	app.add_handler(start_handler)
	app.add_handler(help_handler)
	app.add_handler(keyboard_button_handler)
	app.add_handler(inline_method_handler)
	app.add_handler(echo_handler)
      
	logger.info(f"The bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!") # debugging print
	app.run_polling(poll_interval=3) # read input every 3s
