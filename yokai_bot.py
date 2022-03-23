from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from key import TOKEN
from connect_to_bd import stickers, replies, insert_sticker, in_database


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )

    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.all, do_echo)
    keyboard_handler = MessageHandler(Filters.text('Клавиатура, клавиатура'), keyboard)
    static_handler = MessageHandler(Filters.text('Статистика, статистика'), static)
    sticker_handler = MessageHandler(Filters.sticker, reply_sticker)
    say_smth_handler = MessageHandler(Filters.text, say_smth)
    new_sticker_handler = MessageHandler(Filters.sticker, new_sticker)
    text_handler = MessageHandler(Filters.text, new_keyword)

    dispatcher.add_handler(new_sticker_handler)
    dispatcher.add_handler(text_handler)
    dispatcher.add_handler(say_smth_handler)
    dispatcher.add_handler(sticker_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(static_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    print('Бот успешно запустился')
    updater.idle()


def do_echo(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    surname = update.message.from_user.last_name
    telegram_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    update.message.reply_text(text=f'{text}')
    print(username, ':', text)


def static(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    surname = update.message.from_user.last_name
    telegram_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    update.message.reply_text(
        text=f'Привет, {name} {surname}-@{username}\n'
             f'id: {telegram_id}\n'
             'Приятно познакомится с живым человеком! :)\n'
             'Я — бот.\n'
             'Умею показывать что ты написал.'
    )
    print(username, ':', text)


def keyboard(update: Update, context: CallbackContext) -> None:
    buttons = [
        ['Добавить стикер'],
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
            one_time_keyboard=True,

        )
    )


def reply_sticker(update: Update, context: CallbackContext) -> None:
    sticker = update.message.sticker
    if sticker:
        sticker_id = sticker.file_id
        update.message.reply_sticker(sticker_id)
        print(sticker, sticker_id)


def say_smth(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    text = update.message.text
    for keyword in stickers:
        if keyword in text:
            if stickers[keyword]:
                update.message.reply_sticker(stickers[keyword])
            if replies[keyword]:
                update.message.reply_text(replies[keyword])
    else:
        do_echo(update, context)


def new_sticker(update: Update, context: CallbackContext) -> None:
    sticker_id = update.message.sticker.file_id
    for keyword in stickers:
        if sticker_id == stickers[keyword]:
            update.message.reply_text('у меня тоже такой есть')
            update.message.reply_sticker(sticker_id)
            break
    else:
        context.user_data['new_sticker'] = sticker_id
        update.message.reply_text('введи ключевое слово')


def new_keyword(update: Update, context: CallbackContext) -> None:
    if 'new_sticker' not in context.user_data:
        say_smth(update, context)
    else:
        keyword = update.message.text
        sticker_id = context.user_data['new_sticker']
        insert_sticker(keyword, sticker_id)
        context.user_data.clear()


def meet(update: Update, context: CallbackContext):
    ''' start to add in database:
        id
        name
        sex
        grade
    '''
    telegram_id = update.message.from_user.id
    if in_database(telegram_id):
        pass
    update.message.reply_text(
        'Привет имя введи пжпжпж'
    )
    


def ask_name(update: Update, context: CallbackContext):
    pass


def ask_sex(update: Update, context: CallbackContext):
    pass


def ask_grade(update: Update, context: CallbackContext):
    pass


def greet(update: Update, context: CallbackContext):
    pass




if __name__ == '__main__':
    main()