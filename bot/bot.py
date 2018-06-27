#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import re
import requests
import logging
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


try:
    updater = Updater(token=sys.argv[1])
    dispatcher = updater.dispatcher
except IndexError:
    print('Не задан API token')
    exit()


# Command bot
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Просто пришли мне логин@репозиторий в таком формате.')


# Download repo
def download(login, repo, path_file):
    response = requests.get(f'https://github.com/{login}/{repo}/archive/master.zip')
    if response.status_code == 200:
        with open(path_file, 'wb') as f:
            f.write(response.content)


def request_message(bot, update):
    if '@' in update.message.text:
        login = re.split('@', update.message.text)
        if requests.get(f"https://api.github.com/users/{login[0]}").status_code == 200:
            if requests.get(f"https://api.github.com/repos/{login[0]}/{login[1]}").status_code == 200:
                path_file = f'/data/{login[0]}_{login[1]}.zip'
                try:
                    date = datetime.fromtimestamp(os.stat(f'{path_file}').st_mtime)
                    if (datetime.now() - date).days > 7:
                        download(login[0], login[1], path_file)
                except FileNotFoundError:
                    download(login[0], login[1], path_file)
                finally:
                    date = datetime.fromtimestamp(os.stat(f'{path_file}').st_mtime).strftime('%d.%m.%y %H:%M')
                    bot.send_document(chat_id=update.message.chat_id, document=open(f'{path_file}', 'rb'))
                    response = f'Архив от {date}'
            else:
                response = f'Репозиторий {login[1]} не найден'
        else:
            response = f'Пользователь {login[0]} не найден'
    else:
        response = f'Не правильный формат ввода. Напиши мне логин@репозиторий'
    bot.send_message(chat_id=update.message.chat_id, text=response)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Хендлеры
start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, request_message)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
updater.start_polling(clean=True)
updater.start_webhook ( listen = ' 0.0.0.0 ', port = 8443)
updater.idle()
