import os
import telebot
import logging
import pandas
from dotenv import load_dotenv
from telebot import types


# VARIABLES INITIALIZE


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


# FUNCS FOR BOT

def parse_excel():
    usernames = []
    excel_data = pandas.read_excel('Recipients data.xlsx', sheet_name='Успеваемость')

    for column in excel_data['Логин'].tolist():
        usernames.append(column)

    with open("usernames.txt", "w") as file:
        for user in usernames:
            file.write(f"{user}\n")


def send_docs(msg):
    doc = open("usernames.txt", "rb")
    bot.send_document(msg.chat.id, doc)
    os.remove("usernames.txt")


# BOT LOGIC


@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    api_btn = types.KeyboardButton("API docs")
    github_btn = types.KeyboardButton("Github repository")
    excel_btn = types.KeyboardButton("Extract email from Excel")
    markup.add(api_btn, github_btn, excel_btn)
    bot.send_message(msg.chat.id, text="Hi, {0.first_name}! Im BOT!".format(msg.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def reply(msg):
    if msg.text == "API docs":
        markup = types.InlineKeyboardMarkup()
        btn_api = types.InlineKeyboardButton("API docs", url="https://pytba.readthedocs.io/ru/latest/index.html")
        markup.add(btn_api)
        bot.send_message(msg.chat.id, "Hello, {0.first_name}! Your link is ready :)".format(msg.from_user),
                         reply_markup=markup)
    elif msg.text == "Github repository":
        markup = types.InlineKeyboardMarkup()
        btn_github = types.InlineKeyboardButton("Github repository", url="https://github.com/etoyadadaya/py-automation")
        markup.add(btn_github)
        bot.send_message(msg.chat.id, "Hello, {0.first_name}! Your link is ready :)".format(msg.from_user),
                         reply_markup=markup)
    elif msg.text == "Extract email from Excel":
        markup = types.InlineKeyboardMarkup()
        bot.send_message(msg.chat.id, "Input Excel-file".format(msg.from_user),
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

        bot.reply_to(msg, "saved!")
        parse_excel()
        os.remove("Recipients data.xlsx")
        send_docs(msg)
    except Exception as e:
        bot.reply_to(msg, e)


bot.infinity_polling()
