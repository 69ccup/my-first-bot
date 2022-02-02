from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from key import TOKEN


def main():
    #ловим обноления
    updater = Updater(
        token = TOKEN,
        use_context = True
    )

    #добрый вечер я
    dispatcher = updater.dispatcher

    #обработчик
    echo_handler = MessageHandler(Filters.all, do_echo)
    hello_handler = MessageHandler(Filters.text("пошел нахуй"), react_hello)

    #заргали обработчик ПОРЯДОК ТВАРЬ
    dispatcher.add_handler(hello_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


def do_echo(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    id = update.message.chat_id
    text = update.message.text
    update.message.reply_text(text=f'Твой id = {id}')


def react_hello(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    id = update.message.chat_id
    text = update.message.text
    update.message.reply_text(text=f'Сам пошел нахуй,{name}')


if __name__ == '__main__':
    main()




