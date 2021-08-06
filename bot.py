import logging

from telegram import Update, ForceReply
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

CHANGEPERIOD = range(1)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("BTN", callback_data='btn'),
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('START!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()


def main() -> None:
    updater = Updater("TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    conv = ConversationHandler(
        allow_reentry=True,

        entry_points=[CallbackQueryHandler(help_command, pattern="pattern")],
        states={
            CHANGEPERIOD: [
                MessageHandler(Filters.regex('^Назад'), help_command),
            ],
        },
        
        fallbacks=[],
    )

    dispatcher.add_handler(conv)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
