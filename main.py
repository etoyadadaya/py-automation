import os
import telebot
import logging
from dotenv import load_dotenv
from telebot import types

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    api_btn = types.KeyboardButton("Дока API")
    github_btn = types.KeyboardButton("Github репозиторий")
    markup.add(api_btn, github_btn)
    bot.send_message(msg.chat.id, text="Привет, {0.first_name}! Я тестовый бот!".format(msg.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def reply(msg):
    if msg.text == "Дока API":
        markup = types.InlineKeyboardMarkup()
        btn_api = types.InlineKeyboardButton("Дока API", url="https://pytba.readthedocs.io/ru/latest/index.html")
        markup.add(btn_api)
        bot.send_message(msg.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт".format(msg.from_user),
                         reply_markup=markup)
    elif msg.text == "Github репозиторий":
        markup = types.InlineKeyboardMarkup()
        btn_github = types.InlineKeyboardButton("Ссылка на GitHub", url="https://github.com/etoyadadaya/py-automation")
        markup.add(btn_github)
        bot.send_message(msg.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт".format(msg.from_user),
                         reply_markup=markup)


bot.infinity_polling()
