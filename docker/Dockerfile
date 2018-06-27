FROM ubuntu:latest
MAINTAINER Ilya Khramtsov <ilya@roothub.pw>
RUN apt-get update && apt-get -y install python3 python3-pip git
RUN git clone https://github.com/nuBacuk/telegram-bot.git /telegram && pip3 install -r /telegram/bot/requirement.txt && chmod 777 /telegram/bot/bot.py && mkdir /data
RUN ln -s /telegram/bot/bot.py /usr/bin/bot.py
VOLUME /data
EXPOSE 8443
