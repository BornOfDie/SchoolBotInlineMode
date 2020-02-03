import sys
import time

import telebot
from telebot import types
from settings import *

bot = telebot.TeleBot(API_TOKEN)


def work(schedule: str):
    return '\n'.join(["{}) {}".format(i, a) for i, a in enumerate(schedule.split('\n'), 1)])


for group in lessons:
    for day in lessons[group]:
        lessons[group][day] = work(lessons[group][day])


def logic(inline_query):
    try:
        r = []
        for i, d in enumerate(lessons[inline_query.query].keys()):
            schedule = f'Розклад для {inline_query.query} групи на {d}:\n{lessons[inline_query.query][d]}'
            r.append(types.InlineQueryResultArticle(i, d, types.InputTextMessageContent(schedule)))
        print(r)
        bot.answer_inline_query(inline_query.id, r)
    except Exception as e:
        return e

@bot.message_handler(commands=['id'])
def action_list_sending(message):
    bot.send_message(message.chat.id, message.chat.id)

@bot.inline_handler(lambda query: query.query in lessons)
def query_text(inline_query):
    logic(inline_query)


@bot.message_handler(commands=['start'])
def starting(message):
    markup = types.InlineKeyboardMarkup()
    my_link = types.InlineKeyboardButton(text='Розроблювач', url='https://t.me/ZnerSCHt')
    markup.add(my_link)
    bot.send_message(message.chat.id, GREETING, parse_mode='markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def starting(message):
    bot.send_message(message.chat.id, HELP, parse_mode='markdown')

@bot.message_handler(commands=['commands'])
def starting(message):
    bot.send_message(message.chat.id, COMMANDS, parse_mode='markdown')


@bot.message_handler(commands=['get'])
def get(message):
    if message.chat.type == 'private':
        key = types.InlineKeyboardMarkup()
        for g in lessons:
            btn = types.InlineKeyboardButton(text=g, callback_data=g)
            key.add(btn)
        bot.send_message(message.chat.id, 'Оберіть групу', reply_markup=key)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.message.chat.type == 'private':
        for g in lessons:
            if c.data == g:
                days = types.InlineKeyboardMarkup()
                for d in lessons[c.data]:
                    btn = types.InlineKeyboardButton(text=d, callback_data=d)
                    days.add(btn)
                btn = types.InlineKeyboardButton(text='Повернутись', callback_data='back')
                days.add(btn)
                bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                                      text=f'Розклад для {g} групи', reply_markup=days)

            elif c.data in lessons[group]:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text=lessons[group][c.data])

            elif c.data == 'back':
                key = types.InlineKeyboardMarkup()
                for gr in lessons:
                    btn = types.InlineKeyboardButton(text=gr, callback_data=group)
                    key.add(btn)

                bot.edit_message_text(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    text=GREETING,
                    reply_markup=key
                )


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
