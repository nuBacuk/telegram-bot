import requests
import re
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='529958462:AAEqo08hxFmbAQ_z5e7sS7NfZuBduC5jyOs')
dispatcher = updater.dispatcher


# Command bot
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Просто пришли мне логин@репозиторий в таком формате.')


def download(login, repo):
    response = requests.get(f'https://github.com/{login}/{repo}/archive/master.zip')
    if response.status_code == 200:
        with open(f'{login}_{repo}.zip', 'wb') as f:
            f.write(response.content)


def request_message(bot, update):
    if '@' in update.message.text:
        login = re.split('@', update.message.text)
        if requests.get(f"https://api.github.com/users/{login[0]}").status_code == 200:
            if requests.get(f"https://api.github.com/repos/{login[0]}/{login[1]}").status_code == 200:
                download(login[0], login[1])
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
