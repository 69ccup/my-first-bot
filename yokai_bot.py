from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from key import TOKEN
from openpyxl import load_workbook







def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )

    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.all, do_echo)
    hello_handler = MessageHandler(Filters.text('Привет, привет'), say_hello)
    keyboard_handler = MessageHandler(Filters.text('Клавиатура, клавиатура'), keyboard)

    dispatcher.add_handler(hello_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    print('Бот успешно запустился')
    updater.idle()


def do_echo(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    surname = update.message.from_user.last_name
    telegram_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text if update.message.text else ''
    sticker = update.message.sticker
    if sticker:
        sticker_id = sticker.file_id
        update.message.reply_sticker(sticker_id)
        print(sticker, '\n', sticker_id)
    update.message.reply_text(text=f'{text}')
    print(username, ':', text)


def say_hello(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    surname = update.message.from_user.last_name
    telegram_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text if update.message.text else ''
    update.message.reply_text(
        text=f'Привет, {name} {surname}-@{username}\n'
             f'id: {telegram_id}\n'
             'Приятно познакомится с живым человеком! :)\n'
             'Я — бот.\n'
             'Умею показывать что ты написал.',
        reply_markup=ReplyKeyboardRemove()
    )
    print(username, ':', text)


def keyboard(update: Update, context: CallbackContext) -> None:
    buttons = [
        ['1', '2', '3'],
        ['Привет', 'Пока']
    ]
    keys = ReplyKeyboardMarkup(
        buttons
    )
    update.message.reply_text(
        text='Смотри, у тебя появились кнопки!',
        reply_markup=ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True,
            # one_time_keyboard=True,

        )
    )


if __name__ == '__main__':
    main()