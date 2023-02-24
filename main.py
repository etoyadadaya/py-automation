import os
import telebot
import logging
from dotenv import load_dotenv
from telebot import types
from openpyxl import load_workbook

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


# FUNCS FOR BOT


def parse_excel():
    book = load_workbook("workbook")
    sheet = book.active

    rows = sheet.rows

    headers = [cell.value for cell in next(rows)]

    all_rows = []

    for row in rows:
        data = {}
        for title, cell in zip(headers, row):
            data[title] = cell.value

        all_rows.append(data)

    return all_rows


# BOT LOGIC


@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    api_btn = types.KeyboardButton("Дока API")
    github_btn = types.KeyboardButton("Github репозиторий")
    excel_btn = types.KeyboardButton("Достать почту из Excel файла")
    markup.add(api_btn, github_btn, excel_btn)
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
        bot.send_message(msg.chat.id, "Привет!!!, {0.first_name}! Нажми на кнопку и перейди на сайт".format(msg.from_user),
                         reply_markup=markup)
    elif msg.text == "Достать почту из Excel файла":
        markup = types.InlineKeyboardMarkup()
        bot.send_message(msg.chat.id, "Просто закинь Excel файл".format(msg.from_user),
                         reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_docs(msg):
    try:
        chat_id = msg.chat.id

        file_info = bot.get_file(msg.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = '' + msg.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(msg, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(msg, e)

    all_rows = parse_excel()
    print(all_rows)


bot.infinity_polling()
