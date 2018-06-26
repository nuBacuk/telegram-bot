import os
import time
import re
import requests
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


try:
    with open('token.cfg') as f:
        token = f.readline()

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
except FileNotFoundError:
    print('Файл token.cfg содержащий API token не найден')
    exit()


# Command bot
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Просто пришли мне логин@репозиторий в таком формате.')


# Download repo
def download(login, repo):
    response = requests.get(f'https://github.com/{login}/{repo}/archive/master.zip')
    path_file = f'{login}_{repo}.zip'
    if response.status_code == 200:
        with open(path_file, 'wb') as f:
            f.write(response.content)
    return path_file


def request_message(bot, update):
    if '@' in update.message.text:
        login = re.split('@', update.message.text)
        if requests.get(f"https://api.github.com/users/{login[0]}").status_code == 200:
            if requests.get(f"https://api.github.com/repos/{login[0]}/{login[1]}").status_code == 200:
                path_file = download(login[0], login[1])
                bot.send_document(chat_id=update.message.chat_id, document=open(f'{path_file}', 'rb'))
                date = time.strftime('%d.%m.%y %H:%M', time.gmtime(os.stat(f'{path_file}').st_mtime))
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
updater.idle()
